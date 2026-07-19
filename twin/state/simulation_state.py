from dataclasses import dataclass


@dataclass
class SimulationState:
    """
    Stores the current simulation time state.

    tick:
        Number of completed simulation steps.

    runtime_hours:
        Total simulated operating time in hours.
    """

    tick: int = 0

    runtime_hours: float = 0.0