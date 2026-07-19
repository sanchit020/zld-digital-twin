from dataclasses import dataclass


@dataclass
class HealthState:
    ro_fouling: float = 0.0
    pump_wear: float = 0.0