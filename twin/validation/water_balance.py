def validate_water_balance(state):

    feed = state.process.feed_flow

    permeate = state.process.permeate_flow

    brine = state.process.brine_flow

    error = abs(
        feed - (permeate + brine)
    )

    return error