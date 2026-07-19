from .base_asset import Asset


class Pump(Asset):

    def __init__(
        self,
        nominal_efficiency=0.85
    ):
        self.nominal_efficiency = (
            nominal_efficiency
        )

    def update(self, state, dt):
        feed_flow = max(
            0.0,
            state.process.feed_flow
        )

        operating_pressure = max(
            0.0,
            state.process.operating_pressure
        )

        pump_wear = max(
            0.0,
            state.health.pump_wear
        )

        effective_efficiency = (
            self.nominal_efficiency
            * (
                1.0
                - pump_wear
            )
        )

        effective_efficiency = max(
            0.50,
            min(
                effective_efficiency,
                1.0
            )
        )

        pump_power = (
            feed_flow
            * operating_pressure
            / effective_efficiency
        )

        state.assets.pump_pressure = (
            operating_pressure
        )

        state.assets.pump_power = (
            pump_power
        )

        state.assets.pump_efficiency = (
            effective_efficiency
        )

        wear_rate = 0.005

        state.health.pump_wear += (
            wear_rate
            * dt
        )

        state.health.pump_wear = min(
            state.health.pump_wear,
            0.30
        )

        return state