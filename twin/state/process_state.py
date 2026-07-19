from dataclasses import dataclass


@dataclass
class ProcessState:
    """
    Stores physical process conditions and material-flow variables.
    """

    # Feed-water conditions
    feed_flow: float = 100.0
    feed_tds: float = 38000.0
    feed_temperature: float = 25.0

    # RO operating conditions
    operating_pressure: float = 60.0

    # Fraction, not percentage:
    # 0.45 = 45%
    target_recovery: float = 0.45

    # RO process flows
    permeate_flow: float = 0.0
    brine_flow: float = 0.0

    # ZLD process flows
    zld_feed_flow: float = 0.0
    zld_recovered_water: float = 0.0
    zld_residual_liquid: float = 0.0

    # Whole-plant water recovery
    total_recovered_water: float = 0.0
    overall_water_recovery: float = 0.0