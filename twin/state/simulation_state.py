from dataclasses import dataclass

@dataclass
class SimulationState:

    tick: int = 0
    runtime_hours: float = 0.0