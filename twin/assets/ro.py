from .base_asset import Asset


class RO(Asset):

    def __init__(
        self,
        design_recovery=0.50,
        salt_rejection=0.995
    ):
        self.design_recovery = max(
            0.0,
            min(
                design_recovery,
                1.0
            )
        )

        self.salt_rejection = max(
            0.0,
            min(
                salt_rejection,
                1.0
            )
        )

    def update(self, state, dt):
        feed_flow = max(
            0.0,
            state.process.feed_flow
        )

        feed_tds = max(
            0.0,
            state.process.feed_tds
        )

        feed_temperature = (
            state.process.feed_temperature
        )

        pump_pressure = max(
            0.0,
            state.assets.pump_pressure
        )

        ro_fouling = max(
            0.0,
            min(
                state.health.ro_fouling,
                1.0
            )
        )

        reference_pressure = 60.0

        pressure_factor = (
            pump_pressure
            / reference_pressure
        )

        reference_tds = 38000.0

        if feed_tds > 0.0:
            tds_factor = (
                feed_tds
                / reference_tds
            )
        else:
            tds_factor = 1.0

        tds_factor = max(
            tds_factor,
            0.01
        )

        temperature_factor = (
            1.0
            + (
                feed_temperature
                - 25.0
            )
            * 0.01
        )

        temperature_factor = max(
            temperature_factor,
            0.50
        )

        fouling_factor = (
            1.0
            - ro_fouling
        )

        fouling_factor = max(
            fouling_factor,
            0.10
        )

        recovery_fraction = (
            self.design_recovery
            * pressure_factor
            * temperature_factor
            * fouling_factor
            / tds_factor
        )

        recovery_fraction = max(
            0.10,
            min(
                recovery_fraction,
                0.60
            )
        )

        state.assets.ro_recovery = (
            recovery_fraction
            * 100.0
        )

        permeate_flow = (
            feed_flow
            * recovery_fraction
        )

        brine_flow = (
            feed_flow
            - permeate_flow
        )

        state.process.permeate_flow = (
            permeate_flow
        )

        state.process.brine_flow = (
            brine_flow
        )

        state.assets.ro_permeate_flow = (
            permeate_flow
        )

        state.assets.ro_brine_flow = (
            brine_flow
        )

        permeate_tds = (
            feed_tds
            * (
                1.0
                - self.salt_rejection
            )
        )

        state.assets.permeate_tds = (
            permeate_tds
        )

        feed_salt_load = (
            feed_flow
            * feed_tds
        )

        permeate_salt_load = (
            permeate_flow
            * permeate_tds
        )

        brine_salt_load = max(
            0.0,
            (
                feed_salt_load
                - permeate_salt_load
            )
        )

        if brine_flow > 0.0:
            brine_tds = (
                brine_salt_load
                / brine_flow
            )
        else:
            brine_tds = 0.0

        state.assets.brine_tds = (
            brine_tds
        )

        required_pressure = (
            reference_pressure
            * tds_factor
            * (
                1.0
                + ro_fouling
            )
        )

        state.assets.ro_required_pressure = (
            required_pressure
        )

        fouling_rate = 0.02

        state.health.ro_fouling += (
            fouling_rate
            * dt
        )

        cip_threshold = 0.35

        if (
            state.health.ro_fouling
            >= cip_threshold
        ):
            state.health.ro_fouling = 0.05

        return state