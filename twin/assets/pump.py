from .base_asset import Asset


class Pump(Asset):

    def __init__(
        self,
        design_pressure=60.0,
        efficiency=0.85
    ):
        self.design_pressure = design_pressure
        self.efficiency = efficiency

    def update(self, state, dt):

        flow = state.process.feed_flow

        pressure = self.design_pressure
        effective_efficiency = (self.efficiency*(1 -state.health.pump_wear))
        effective_efficiency = max(0.5,effective_efficiency)
        hydraulic_power = (
            flow * pressure
        ) / effective_efficiency

        state.assets.pump_pressure = pressure
        state.assets.pump_power = hydraulic_power
        # hydraulic_power = (flow*pressure) / effective_efficiency
        state.assets.pump_efficiency = (effective_efficiency)
        state.health.pump_wear += (0.005 * dt)
        state.health.pump_wear = min(state.health.pump_wear,0.30)
        return state