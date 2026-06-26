from dataclasses import dataclass


@dataclass
class EconomicState:

    energy_cost: float = 0.0
    net_operating_cost: float = 0.0
    cumulative_energy_cost: float = 0.0

    px_savings: float = 0.0

    cumulative_px_savings: float = 0.0

    power_price: float = 8.0