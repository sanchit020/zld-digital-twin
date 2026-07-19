def validate_water_balance(
    state,
    tolerance=1e-6
):
    feed = state.process.feed_flow

    permeate = state.process.permeate_flow

    brine = state.process.brine_flow

    zld_feed = state.process.zld_feed_flow

    zld_recovered = (
        state.process.zld_recovered_water
    )

    zld_residual = (
        state.process.zld_residual_liquid
    )

    ro_balance_error = abs(
        feed
        - (
            permeate
            + brine
        )
    )

    zld_active = (
        state.assets.brine_to_zld > 0.0
    )

    if zld_active:
        zld_balance_error = abs(
            zld_feed
            - (
                zld_recovered
                + zld_residual
            )
        )
    else:
        zld_balance_error = 0.0

    overall_balance_error = abs(
        feed
        - (
            permeate
            + zld_recovered
            + zld_residual
        )
    )

    ro_valid = (
        ro_balance_error
        <= tolerance
    )

    zld_valid = (
        zld_balance_error
        <= tolerance
    )

    overall_valid = (
        overall_balance_error
        <= tolerance
    )

    all_valid = (
        ro_valid
        and zld_valid
        and overall_valid
    )

    return {
        "ro_balance_error": ro_balance_error,
        "zld_balance_error": zld_balance_error,
        "overall_balance_error": overall_balance_error,
        "ro_valid": ro_valid,
        "zld_valid": zld_valid,
        "overall_valid": overall_valid,
        "all_valid": all_valid
    }