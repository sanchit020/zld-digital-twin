from .base_asset import Asset


class PX(Asset):

    def update(self, state, dt):
        px_enabled = (
            state.assets.px_enabled
        )

        px_efficiency = max(
            0.0,
            min(
                state.assets.px_efficiency,
                1.0
            )
        )

        if not px_enabled:
            state.assets.px_recovered_power = 0.0
            return state

        brine_flow = max(
            0.0,
            state.assets.ro_brine_flow
        )

        brine_pressure = max(
            0.0,
            state.assets.pump_pressure
        )

        reference_pressure = 60.0

        pressure_factor = (
            brine_pressure
            / reference_pressure
        )

        recovered_power = (
            brine_flow
            * brine_pressure
            * pressure_factor
            * px_efficiency
        )

        recovered_power = max(
            0.0,
            recovered_power
        )

        recovered_power = min(
            recovered_power,
            state.assets.pump_power
        )

        state.assets.px_recovered_power = (
            recovered_power
        )

        degradation_rate = 0.002

        state.assets.px_efficiency -= (
            degradation_rate
            * dt
        )

        state.assets.px_efficiency = max(
            state.assets.px_efficiency,
            0.80
        )

        return state