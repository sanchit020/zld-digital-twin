from dataclasses import dataclass

from twin.state.process_state import ProcessState
from twin.state.asset_state import AssetState
from twin.state.health_state import HealthState
from twin.state.economic_state import EconomicState
from twin.state.simulation_state import SimulationState


@dataclass
class PlantState:
    process: ProcessState
    assets: AssetState
    health: HealthState
    economics: EconomicState
    simulation: SimulationState