import math

from twin.assets.pump import Pump
from twin.assets.ro import RO
from twin.assets.px import PX
from twin.assets.zld import ZLD


class SimulationKernel:

    def __init__(self, scenario=None):
        self.scenario = scenario or {}

        process_config = self.scenario.get(
            "process",
            {}
        )

        zld_config = self.scenario.get(
            "zld",
            {}
        )

        self.base_feed_tds = process_config.get(
            "feed_tds",
            38000.0
        )

        self.base_feed_temperature = process_config.get(
            "feed_temperature",
            25.0
        )

        self.pump = Pump()
        self.ro = RO()
        self.px = PX()

        self.zld = ZLD(
            enabled=zld_config.get(
                "enabled",
                True
            ),
            water_recovery=zld_config.get(
                "water_recovery",
                0.90
            ),
            specific_energy=zld_config.get(
                "specific_energy",
                20.0
            )
        )

        self.NORMAL_POWER_PRICE = 8.0
        self.PEAK_POWER_PRICE = 12.0

    def step(self, state, dt):
        hour = (
            state.simulation.runtime_hours
            % 24.0
        )

        state.process.feed_tds = (
            self.base_feed_tds
            + 3000.0
            * math.sin(
                2.0
                * math.pi
                * hour
                / 24.0
            )
        )

        state.process.feed_temperature = (
            self.base_feed_temperature
            + 3.0
            * math.sin(
                2.0
                * math.pi
                * (hour - 6.0)
                / 24.0
            )
        )

        target_recovery = (
            state.process.target_recovery
        )

        actual_recovery = (
            state.assets.ro_recovery
            / 100.0
        )

        if actual_recovery < target_recovery:
            state.process.operating_pressure += (
                0.5
            )

        elif actual_recovery > target_recovery:
            state.process.operating_pressure -= (
                0.5
            )

        state.process.operating_pressure = max(
            55.0,
            min(
                state.process.operating_pressure,
                70.0
            )
        )

        state = self.pump.update(
            state,
            dt
        )

        state = self.ro.update(
            state,
            dt
        )

        state = self.px.update(
            state,
            dt
        )

        state.assets.net_power = max(
            0.0,
            (
                state.assets.pump_power
                - state.assets.px_recovered_power
            )
        )

        state = self.zld.update(
            state,
            dt
        )

        state.assets.total_plant_power = (
            state.assets.net_power
            + state.assets.zld_power
        )

        saved_power = max(
            0.0,
            state.assets.px_recovered_power
        )

        energy_saved = (
            saved_power
            * dt
        )

        ro_energy_used = (
            state.assets.net_power
            * dt
        )

        zld_energy_used = (
            state.assets.zld_energy_consumption
        )

        total_energy_used = (
            ro_energy_used
            + zld_energy_used
        )

        if 18.0 <= hour < 22.0:
            current_price = (
                self.PEAK_POWER_PRICE
            )
        else:
            current_price = (
                self.NORMAL_POWER_PRICE
            )

        state.economics.power_price = (
            current_price
        )

        ro_energy_cost = (
            ro_energy_used
            * current_price
        )

        state.economics.ro_energy_cost = (
            ro_energy_cost
        )

        state.economics.cumulative_ro_energy_cost += (
            ro_energy_cost
        )

        zld_energy_cost = (
            zld_energy_used
            * current_price
        )

        state.economics.zld_energy_cost = (
            zld_energy_cost
        )

        state.economics.cumulative_zld_energy_cost += (
            zld_energy_cost
        )

        total_energy_cost = (
            total_energy_used
            * current_price
        )

        state.economics.energy_cost = (
            total_energy_cost
        )

        state.economics.cumulative_energy_cost += (
            total_energy_cost
        )

        px_savings = (
            energy_saved
            * current_price
        )

        state.economics.px_savings = (
            px_savings
        )

        state.economics.cumulative_px_savings += (
            px_savings
        )

        state.economics.net_operating_cost = (
            state.economics.cumulative_energy_cost
        )

        state.simulation.tick += 1

        state.simulation.runtime_hours += (
            dt
        )

        if state.simulation.tick % 50 == 0:
            print(
                f"Hour={state.simulation.runtime_hours:.2f}, "
                f"TDS={state.process.feed_tds:.0f}, "
                f"Temp={state.process.feed_temperature:.1f}, "
                f"Pressure={state.process.operating_pressure:.1f}, "
                f"RORecovery={state.assets.ro_recovery:.2f}%, "
                f"BrineTDS={state.assets.brine_tds:.0f}, "
                f"Fouling={state.health.ro_fouling:.3f}, "
                f"PXRecovered={state.assets.px_recovered_power:.2f}, "
                f"RONetPower={state.assets.net_power:.2f}, "
                f"ZLDWater={state.assets.zld_water_recovered:.2f}, "
                f"ZLDSalt={state.assets.zld_solid_residue:.2f}, "
                f"ZLDPower={state.assets.zld_power:.2f}, "
                f"TotalPower={state.assets.total_plant_power:.2f}, "
                f"OverallRecovery="
                f"{state.process.overall_water_recovery:.2f}%"
            )

        return state