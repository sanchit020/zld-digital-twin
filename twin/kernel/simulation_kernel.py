from twin.assets.pump import Pump
from twin.assets.ro import RO
from twin.assets.px import PX


class SimulationKernel:

    def __init__(self):

        self.pump = Pump()
        self.ro = RO()
        self.px = PX()

        self.POWER_PRICE = 8.0  # ₹/kWh

    def step(self, state, dt):

        # --------------------
        # Process Simulation
        # --------------------

        state = self.pump.update(state, dt)

        state = self.ro.update(state, dt)

        state = self.px.update(state, dt)

        # --------------------
        # Energy Balance
        # --------------------

        state.assets.net_power = (
            state.assets.pump_power
            - state.assets.px_recovered_power
        )

        # --------------------
        # Economic Calculations
        # --------------------

        baseline_power = state.assets.pump_power

        actual_power = state.assets.net_power

        saved_power = (
            baseline_power
            - actual_power
        )

        # kWh consumed this tick
        energy_used = (
            actual_power
            * dt
        )

        # kWh saved this tick
        energy_saved = (
            saved_power
            * dt
        )

        cost = (
            energy_used
            * self.POWER_PRICE
        )

        savings = (
            energy_saved
            * self.POWER_PRICE
        )

        state.economics.energy_cost = cost

        state.economics.cumulative_energy_cost += cost

        state.economics.px_savings = savings

        state.economics.cumulative_px_savings += savings

        # --------------------
        # Simulation Clock
        # --------------------

        state.simulation.tick += 1

        state.simulation.runtime_hours += dt
        state.economics.net_operating_cost = (state.economics.cumulative_energy_cost-state.economics.cumulative_px_savings)
        return state