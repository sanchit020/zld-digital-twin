import argparse
import os

from twin.scenarios.scenario_runner import run_scenario


SCENARIOS = {
    "baseline": "twin/configs/baseline.yaml",
    "high_tds": "twin/configs/high_tds.yaml",
    "aged_assets": "twin/configs/aged_assets.yaml",
    "px_failure": "twin/configs/px_failure.yaml",
}


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Run the Sorek-inspired RO + PX + ZLD "
            "Digital Twin simulation."
        )
    )

    parser.add_argument(
        "--scenario",
        choices=SCENARIOS.keys(),
        default="baseline",
        help=(
            "Simulation scenario to execute. "
            "Default: baseline"
        )
    )

    parser.add_argument(
        "--ticks",
        type=int,
        default=1000,
        help=(
            "Number of simulation ticks to execute. "
            "Default: 1000"
        )
    )

    args = parser.parse_args()

    if args.ticks <= 0:
        parser.error(
            "--ticks must be greater than zero."
        )

    project_root = os.path.dirname(
        os.path.abspath(__file__)
    )

    relative_config_path = SCENARIOS[
        args.scenario
    ]

    config_path = os.path.join(
        project_root,
        relative_config_path
    )

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Scenario configuration not found: "
            f"{config_path}"
        )

    print("=" * 60)

    print(
        "SOREK-INSPIRED RO + PX + ZLD DIGITAL TWIN"
    )

    print("=" * 60)

    print(
        f"Scenario : {args.scenario}"
    )

    print(
        f"Ticks    : {args.ticks}"
    )

    print(
        f"Config   : {relative_config_path}"
    )

    print("=" * 60)

    final_state = run_scenario(
        config_path=config_path,
        ticks=args.ticks
    )

    print()

    print("=" * 60)

    print(
        "FINAL SIMULATION SUMMARY"
    )

    print("=" * 60)

    print(
        f"Runtime Hours: "
        f"{final_state.simulation.runtime_hours:.3f}"
    )

    print(
        f"Final Feed TDS: "
        f"{final_state.process.feed_tds:.2f} mg/L"
    )

    print(
        f"Operating Pressure: "
        f"{final_state.process.operating_pressure:.2f} bar"
    )

    print(
        f"RO Recovery: "
        f"{final_state.assets.ro_recovery:.2f}%"
    )

    print(
        f"RO Permeate Flow: "
        f"{final_state.assets.ro_permeate_flow:.2f}"
    )

    print(
        f"RO Brine Flow: "
        f"{final_state.assets.ro_brine_flow:.2f}"
    )

    print(
        f"Brine TDS: "
        f"{final_state.assets.brine_tds:.2f} mg/L"
    )

    print("-" * 60)

    print(
        f"PX Recovered Power: "
        f"{final_state.assets.px_recovered_power:.2f}"
    )

    print(
        f"PX Efficiency: "
        f"{final_state.assets.px_efficiency:.4f}"
    )

    print(
        f"RO/PX Net Power: "
        f"{final_state.assets.net_power:.2f}"
    )

    print("-" * 60)

    print(
        f"Brine Sent to ZLD: "
        f"{final_state.assets.brine_to_zld:.2f}"
    )

    print(
        f"ZLD Water Recovered: "
        f"{final_state.assets.zld_water_recovered:.2f}"
    )

    print(
        f"ZLD Residual Liquid: "
        f"{final_state.assets.zld_residual_liquid:.2f}"
    )

    print(
        f"Estimated Salt Load: "
        f"{final_state.assets.zld_solid_residue:.2f} kg/h"
    )

    print(
        f"ZLD Power: "
        f"{final_state.assets.zld_power:.2f}"
    )

    print("-" * 60)

    print(
        f"Total Recovered Water: "
        f"{final_state.process.total_recovered_water:.2f}"
    )

    print(
        f"Overall Water Recovery: "
        f"{final_state.process.overall_water_recovery:.2f}%"
    )

    print(
        f"Total Plant Power: "
        f"{final_state.assets.total_plant_power:.2f}"
    )

    print("-" * 60)

    print(
        f"Cumulative RO Energy Cost: "
        f"{final_state.economics.cumulative_ro_energy_cost:.2f}"
    )

    print(
        f"Cumulative ZLD Energy Cost: "
        f"{final_state.economics.cumulative_zld_energy_cost:.2f}"
    )

    print(
        f"Cumulative Total Energy Cost: "
        f"{final_state.economics.cumulative_energy_cost:.2f}"
    )

    print(
        f"Cumulative PX Savings: "
        f"{final_state.economics.cumulative_px_savings:.2f}"
    )

    print(
        f"Net Operating Cost: "
        f"{final_state.economics.net_operating_cost:.2f}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()