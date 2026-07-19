from .base_asset import Asset


class ZLD(Asset):

    def __init__(
        self,
        enabled=True,
        water_recovery=0.90,
        specific_energy=20.0
    ):
        self.enabled = enabled

        self.water_recovery = max(
            0.0,
            min(
                water_recovery,
                1.0
            )
        )

        self.specific_energy = max(
            0.0,
            specific_energy
        )

    def update(self, state, dt):
        brine_flow = max(
            0.0,
            state.assets.ro_brine_flow
        )

        brine_tds = max(
            0.0,
            state.assets.brine_tds
        )

        if not self.enabled:
            state.assets.brine_to_zld = 0.0
            state.assets.zld_water_recovered = 0.0

            state.assets.zld_residual_liquid = (
                brine_flow
            )

            state.assets.zld_recovery = 0.0
            state.assets.zld_solid_residue = 0.0
            state.assets.zld_power = 0.0
            state.assets.zld_energy_consumption = 0.0

            state.process.zld_feed_flow = 0.0
            state.process.zld_recovered_water = 0.0

            state.process.zld_residual_liquid = (
                brine_flow
            )

            state.process.total_recovered_water = (
                state.process.permeate_flow
            )

            if state.process.feed_flow > 0.0:
                state.process.overall_water_recovery = (
                    state.process.total_recovered_water
                    / state.process.feed_flow
                    * 100.0
                )
            else:
                state.process.overall_water_recovery = 0.0

            return state

        state.assets.brine_to_zld = (
            brine_flow
        )

        state.process.zld_feed_flow = (
            brine_flow
        )

        recovered_water = (
            brine_flow
            * self.water_recovery
        )

        residual_liquid = (
            brine_flow
            - recovered_water
        )

        state.assets.zld_water_recovered = (
            recovered_water
        )

        state.assets.zld_residual_liquid = (
            residual_liquid
        )

        state.assets.zld_recovery = (
            self.water_recovery
            * 100.0
        )

        state.process.zld_recovered_water = (
            recovered_water
        )

        state.process.zld_residual_liquid = (
            residual_liquid
        )

        salt_mass = (
            brine_flow
            * brine_tds
            / 1000.0
        )

        state.assets.zld_solid_residue = (
            salt_mass
        )

        zld_power = (
            brine_flow
            * self.specific_energy
        )

        state.assets.zld_power = (
            zld_power
        )

        zld_energy = (
            zld_power
            * dt
        )

        state.assets.zld_energy_consumption = (
            zld_energy
        )

        total_recovered_water = (
            state.process.permeate_flow
            + recovered_water
        )

        state.process.total_recovered_water = (
            total_recovered_water
        )

        if state.process.feed_flow > 0.0:
            overall_recovery = (
                total_recovered_water
                / state.process.feed_flow
                * 100.0
            )
        else:
            overall_recovery = 0.0

        overall_recovery = max(
            0.0,
            min(
                overall_recovery,
                100.0
            )
        )

        state.process.overall_water_recovery = (
            overall_recovery
        )

        return state