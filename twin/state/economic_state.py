from dataclasses import dataclass


@dataclass
class EconomicState:
    power_price: float = 0.0

    energy_cost: float = 0.0
    ro_energy_cost: float = 0.0
    zld_energy_cost: float = 0.0

    cumulative_energy_cost: float = 0.0
    cumulative_ro_energy_cost: float = 0.0
    cumulative_zld_energy_cost: float = 0.0

    px_savings: float = 0.0
    cumulative_px_savings: float = 0.0

    net_operating_cost: float = 0.0