from dataclasses import dataclass


@dataclass
class AssetState:
    pump_pressure: float = 60.0
    pump_power: float = 0.0
    pump_efficiency: float = 0.85

    ro_recovery: float = 0.0
    ro_permeate_flow: float = 0.0
    ro_brine_flow: float = 0.0
    permeate_tds: float = 0.0
    brine_tds: float = 0.0
    ro_required_pressure: float = 0.0

    px_enabled: bool = True
    px_efficiency: float = 0.96
    px_recovered_power: float = 0.0

    net_power: float = 0.0

    brine_to_zld: float = 0.0
    zld_water_recovered: float = 0.0
    zld_residual_liquid: float = 0.0
    zld_recovery: float = 0.0
    zld_solid_residue: float = 0.0
    zld_power: float = 0.0
    zld_energy_consumption: float = 0.0

    total_plant_power: float = 0.0