from twin.state.process_state import ProcessState
from twin.state.asset_state import AssetState
from twin.state.health_state import HealthState
from twin.state.economic_state import EconomicState
from twin.state.simulation_state import SimulationState
from twin.state.plant_state import PlantState

from twin.kernel.simulation_kernel import SimulationKernel
from twin.kernel.clock import SimulationClock

from twin.scenarios.scenario_loader import load_scenario
from twin.storage.influx_writer import InfluxWriter


def print_progress(state):

    print(f"Tick: {state.simulation.tick}")

    print(
        f"Recovery: "
        f"{state.assets.ro_recovery:.2f}%"
    )

    print(
        f"Net Power: "
        f"{state.assets.net_power:.2f}"
    )

    print(
        f"RO Fouling: "
        f"{state.health.ro_fouling:.4f}"
    )

    print(
        f"Pump Wear: "
        f"{state.health.pump_wear:.4f}"
    )

    print(
        f"PX Efficiency: "
        f"{state.assets.px_efficiency:.3f}"
    )

    print("-" * 30)


def run_scenario(config_path, ticks=1000):

    scenario = load_scenario(config_path)

    state = PlantState(
        process=ProcessState(
            feed_flow=scenario["process"]["feed_flow"],
            feed_tds=scenario["process"]["feed_tds"],
            feed_temperature=scenario["process"]["feed_temperature"]
        ),
        assets=AssetState(
            pump_pressure=scenario["assets"]["pump_pressure"],
            px_enabled=scenario["assets"]["px_enabled"]
        ),
        health=HealthState(
            ro_fouling=scenario["health"]["ro_fouling"],
            pump_wear=scenario["health"]["pump_wear"],
            px_efficiency=scenario["health"]["px_efficiency"]
        ),
        economics=EconomicState(),
        simulation=SimulationState()
    )

    kernel = SimulationKernel()
    clock = SimulationClock()

    # Create Influx writer
    writer = InfluxWriter()

    for _ in range(ticks):

        state = kernel.step(
            state,
            clock.dt_hours
        )

        # Write every simulation tick to InfluxDB
        writer.write_state(state)

        if state.simulation.tick % 100 == 0:
            print_progress(state)

    return state