from twin.scenarios.scenario_loader import load_scenario

from twin.state.plant_state import PlantState
from twin.state.process_state import ProcessState
from twin.state.asset_state import AssetState
from twin.state.health_state import HealthState
from twin.state.economic_state import EconomicState
from twin.state.simulation_state import SimulationState

from twin.kernel.simulation_kernel import SimulationKernel
from twin.kernel.clock import SimulationClock

from twin.validation.water_balance import validate_water_balance

from twin.storage.influx_writer import InfluxWriter


def run_scenario(
    config_path,
    ticks=1000
):
    if ticks <= 0:
        raise ValueError(
            "Number of simulation ticks must be "
            "greater than zero."
        )

    scenario = load_scenario(
        config_path
    )

    process_config = scenario[
        "process"
    ]

    asset_config = scenario[
        "assets"
    ]

    health_config = scenario[
        "health"
    ]

    zld_config = scenario[
        "zld"
    ]

    process_state = ProcessState(
        feed_flow=process_config[
            "feed_flow"
        ],

        feed_tds=process_config[
            "feed_tds"
        ],

        feed_temperature=process_config[
            "feed_temperature"
        ],

        operating_pressure=process_config.get(
            "operating_pressure",
            asset_config["pump_pressure"]
        ),

        target_recovery=process_config.get(
            "target_recovery",
            0.45
        )
    )

    asset_state = AssetState(
        pump_pressure=asset_config[
            "pump_pressure"
        ],

        px_enabled=asset_config[
            "px_enabled"
        ],

        px_efficiency=health_config[
            "px_efficiency"
        ]
    )

    health_state = HealthState(
        ro_fouling=health_config[
            "ro_fouling"
        ],

        pump_wear=health_config[
            "pump_wear"
        ]
    )

    economic_state = EconomicState()

    simulation_state = SimulationState(
        tick=0,
        runtime_hours=0.0
    )

    state = PlantState(
        process=process_state,
        assets=asset_state,
        health=health_state,
        economics=economic_state,
        simulation=simulation_state
    )

    kernel = SimulationKernel(
        scenario=scenario
    )

    clock = SimulationClock(
        dt_seconds=10.0
    )

    writer = InfluxWriter()

    print()

    print(
        "Starting simulation..."
    )

    print(
        f"Feed Flow: "
        f"{state.process.feed_flow}"
    )

    print(
        f"Base Feed TDS: "
        f"{state.process.feed_tds} mg/L"
    )

    print(
        f"Base Feed Temperature: "
        f"{state.process.feed_temperature} °C"
    )

    print(
        f"Initial Operating Pressure: "
        f"{state.process.operating_pressure} bar"
    )

    print(
        f"Target RO Recovery: "
        f"{state.process.target_recovery * 100:.1f}%"
    )

    print(
        f"PX Enabled: "
        f"{state.assets.px_enabled}"
    )

    print(
        f"Initial PX Efficiency: "
        f"{state.assets.px_efficiency:.3f}"
    )

    print(
        f"ZLD Enabled: "
        f"{zld_config['enabled']}"
    )

    print(
        f"ZLD Water Recovery Setting: "
        f"{zld_config['water_recovery'] * 100:.1f}%"
    )

    print(
        f"ZLD Specific Energy: "
        f"{zld_config['specific_energy']} kWh/m3"
    )

    print()

    try:
        for _ in range(ticks):
            state = kernel.step(
                state,
                clock.dt_hours
            )

            balance = validate_water_balance(
                state
            )

            if not balance["all_valid"]:
                raise RuntimeError(
                    "Water balance validation failed at "
                    f"tick "
                    f"{state.simulation.tick}. "

                    f"RO error="
                    f"{balance['ro_balance_error']:.8f}, "

                    f"ZLD error="
                    f"{balance['zld_balance_error']:.8f}, "

                    f"Overall error="
                    f"{balance['overall_balance_error']:.8f}"
                )

            writer.write_state(
                state
            )

        final_balance = validate_water_balance(
            state
        )

        print()

        print(
            "-" * 60
        )

        print(
            "WATER BALANCE VALIDATION"
        )

        print(
            "-" * 60
        )

        print(
            f"RO Balance Error: "
            f"{final_balance['ro_balance_error']:.10f}"
        )

        print(
            f"ZLD Balance Error: "
            f"{final_balance['zld_balance_error']:.10f}"
        )

        print(
            f"Overall Balance Error: "
            f"{final_balance['overall_balance_error']:.10f}"
        )

        print(
            f"Validation Passed: "
            f"{final_balance['all_valid']}"
        )

        print(
            "-" * 60
        )

    finally:
        writer.close()

    return state