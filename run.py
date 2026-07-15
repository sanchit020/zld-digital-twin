import sys

from twin.scenarios.scenario_runner import run_scenario
from twin.validation.water_balance import validate_water_balance
from twin.storage.influx_writer import InfluxWriter


scenario_name = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "baseline"
)
config_path = (
    f"twin/configs/{scenario_name}.yaml"
)
state = run_scenario(
    config_path,
    ticks=1000
)

writer = InfluxWriter()

writer.write_state(state)

print("\nSCENARIO REPORT")
print("------------------")

print(f"Scenario: {scenario_name}")

print(
    f"Recovery: "
    f"{state.assets.ro_recovery:.2f}%"
)

print(
    f"Net Power: "
    f"{state.assets.net_power:.2f}"
)

print(
    f"Energy Cost: "
    f"₹{state.economics.cumulative_energy_cost:.2f}"
)

print(
    f"PX Savings: "
    f"₹{state.economics.cumulative_px_savings:.2f}"
)

print(
    f"Net Operating Cost: "
    f"₹{state.economics.net_operating_cost:.2f}"
)

error = validate_water_balance(state)

print(
    f"Water Balance Error: "
    f"{error}"
)