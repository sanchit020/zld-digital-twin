from .base_asset import Asset


class RO(Asset):

    def __init__(
        self,
        design_recovery=0.50,
        salt_rejection=0.995
    ):

        self.design_recovery = design_recovery
        self.salt_rejection = salt_rejection

    def update(self, state, dt):

        feed_flow = state.process.feed_flow

        fouling_factor = (1.0 -state.health.ro_fouling)
        tds_factor = (state.process.feed_tds/ 25000)
        required_pressure = (state.assets.pump_pressure*(1 +state.health.ro_fouling))
        state.assets.ro_required_pressure = (required_pressure)
        recovery = (
        self.design_recovery
        /tds_factor
        )
        recovery*=fouling_factor
        recovery = max(
        0.10,
        min(recovery, 0.60)
        )
        permeate_flow = feed_flow * recovery
        permeate_tds = (state.process.feed_tds*(1 -self.salt_rejection))
        state.assets.permeate_tds = (permeate_tds)
        brine_flow = feed_flow - permeate_flow

        state.assets.ro_recovery = recovery * 100

        state.assets.ro_permeate_flow = permeate_flow

        state.assets.ro_brine_flow = brine_flow

        state.process.permeate_flow = permeate_flow

        state.process.brine_flow = brine_flow
        state.health.ro_fouling += (0.05 * dt)
        state.health.ro_fouling = min(
        state.health.ro_fouling,
        0.5
        )

        return state