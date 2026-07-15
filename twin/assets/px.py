from .base_asset import Asset


class PX(Asset):

    def __init__(
        self,
        efficiency=0.96
    ):

        self.efficiency = efficiency

    def update(self, state, dt):
        if not state.assets.px_enabled:

            state.assets.px_recovered_power = 0.0
            return state
        brine_flow = (state.assets.ro_brine_flow)

        brine_pressure = (state.assets.pump_pressure)
        pressure_factor = (
            brine_pressure
            / 60
        )

        recovered_power = (
            brine_flow
            * brine_pressure
            * pressure_factor
            * state.health.px_efficiency
        )
        state.assets.px_recovered_power = (recovered_power)
        state.health.px_efficiency -= (0.002 * dt)

        state.health.px_efficiency = max(0.80,
        state.health.px_efficiency
        )
        state.assets.px_efficiency = (
        state.health.px_efficiency
        )
        return state