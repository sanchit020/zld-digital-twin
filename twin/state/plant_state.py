from dataclasses import dataclass

from .process_state import ProcessState
from .asset_state import AssetState
from .health_state import HealthState
from .economic_state import EconomicState
from .simulation_state import SimulationState

@dataclass
class PlantState:

    process: ProcessState
    assets: AssetState
    health: HealthState
    economics: EconomicState
    simulation: SimulationState