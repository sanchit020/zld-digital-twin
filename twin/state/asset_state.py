from dataclasses import dataclass

@dataclass
class AssetState:

    pump_pressure: float = 60.0

    pump_power: float = 0.0

    pump_efficiency: float = 0.85

    ro_recovery: float = 0.0
    ro_permeate_flow: float = 0.0
    ro_brine_flow: float = 0.0

    px_recovered_power: float = 0.0
    px_efficiency: float = 0.96

    net_power: float = 0.0

    px_enabled: bool = True