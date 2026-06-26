from dataclasses import dataclass

@dataclass
class HealthState:

    pump_wear: float = 0.0

    ro_fouling: float = 0.0

    px_efficiency: float = 0.96