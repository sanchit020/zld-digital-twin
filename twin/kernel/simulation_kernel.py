from twin.assets.pump import Pump
from twin.assets.ro import RO
from twin.assets.px import PX
import math

class SimulationKernel:

    def __init__(self):

        self.pump = Pump()
        self.ro = RO()
        self.px = PX()

        self.POWER_PRICE = 8.0 

    def step(self, state, dt):
        

        hour = state.simulation.runtime_hours % 24

        state.process.feed_tds = (
            38000
            + 3000 * math.sin(
                2 * math.pi * hour / 24
            )
        )

        state.process.feed_temperature = (
            25
            + 3 * math.sin(
                2 * math.pi * (hour - 6) / 24
            )
        )
        target_recovery = state.process.target_recovery

        if hasattr(state.assets, "ro_recovery"):

            actual_recovery = (
                state.assets.ro_recovery / 100
            )

            if actual_recovery < target_recovery:
                state.process.operating_pressure += 0.5

            elif actual_recovery > target_recovery:
                state.process.operating_pressure -= 0.5

        state.process.operating_pressure = max(
            55,
            min(
                70,
                state.process.operating_pressure
            )
        )


        state = self.pump.update(state, dt)

        state = self.ro.update(state, dt)

        state = self.px.update(state, dt)



        state.assets.net_power = (
            state.assets.pump_power
            - state.assets.px_recovered_power
        )


        baseline_power = state.assets.pump_power

        actual_power = state.assets.net_power

        saved_power = (
            baseline_power
            - actual_power
        )

        energy_used = (
            actual_power
            * dt
        )


        energy_saved = (
            saved_power
            * dt
        )

        hour = (
            state.simulation.runtime_hours
            % 24
        )

        if 18 <= hour <= 22:
            current_price = 12
        else:
            current_price = 8

        cost = (
            energy_used
            * current_price
        )

        savings = (
            energy_saved
            * self.POWER_PRICE
        )

        state.economics.energy_cost = cost

        state.economics.cumulative_energy_cost += cost

        state.economics.px_savings = savings

        state.economics.cumulative_px_savings += savings


        state.simulation.tick += 1

        state.simulation.runtime_hours += dt
        state.economics.net_operating_cost = (state.economics.cumulative_energy_cost-state.economics.cumulative_px_savings)
        if state.simulation.tick % 50 == 0:
            print(
                f"Hour={state.simulation.runtime_hours:.1f}, "
                f"TDS={state.process.feed_tds:.0f}, "
                f"Temp={state.process.feed_temperature:.1f}, "
                f"Pressure={state.process.operating_pressure:.1f}, "
                f"Recovery={state.assets.ro_recovery:.2f}, "
                f"Fouling={state.health.ro_fouling:.2f}"
            )
        return state