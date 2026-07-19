import yaml


def load_scenario(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        scenario = yaml.safe_load(file)

    if not isinstance(scenario, dict):
        raise ValueError(
            "Scenario YAML must contain a dictionary/object "
            "at the root level."
        )

    required_sections = [
        "process",
        "assets",
        "health"
    ]

    for section in required_sections:
        if section not in scenario:
            raise ValueError(
                f"Scenario is missing required section: "
                f"'{section}'"
            )

        if not isinstance(
            scenario[section],
            dict
        ):
            raise ValueError(
                f"Scenario section '{section}' "
                f"must contain key-value pairs."
            )

    process = scenario["process"]

    required_process_fields = [
        "feed_flow",
        "feed_tds",
        "feed_temperature"
    ]

    for field in required_process_fields:
        if field not in process:
            raise ValueError(
                f"Missing required process field: "
                f"'{field}'"
            )

    if process["feed_flow"] <= 0:
        raise ValueError(
            "feed_flow must be greater than zero."
        )

    if process["feed_tds"] < 0:
        raise ValueError(
            "feed_tds cannot be negative."
        )

    operating_pressure = process.get(
        "operating_pressure",
        60.0
    )

    if operating_pressure <= 0:
        raise ValueError(
            "operating_pressure must be greater than zero."
        )

    target_recovery = process.get(
        "target_recovery",
        0.45
    )

    if not 0.0 < target_recovery < 1.0:
        raise ValueError(
            "target_recovery must be between 0 and 1."
        )

    assets = scenario["assets"]

    required_asset_fields = [
        "pump_pressure",
        "px_enabled"
    ]

    for field in required_asset_fields:
        if field not in assets:
            raise ValueError(
                f"Missing required asset field: "
                f"'{field}'"
            )

    if assets["pump_pressure"] <= 0:
        raise ValueError(
            "pump_pressure must be greater than zero."
        )

    if not isinstance(
        assets["px_enabled"],
        bool
    ):
        raise ValueError(
            "px_enabled must be true or false."
        )

    health = scenario["health"]

    required_health_fields = [
        "ro_fouling",
        "pump_wear",
        "px_efficiency"
    ]

    for field in required_health_fields:
        if field not in health:
            raise ValueError(
                f"Missing required health field: "
                f"'{field}'"
            )

    if not 0.0 <= health["ro_fouling"] <= 1.0:
        raise ValueError(
            "ro_fouling must be between 0 and 1."
        )

    if not 0.0 <= health["pump_wear"] <= 1.0:
        raise ValueError(
            "pump_wear must be between 0 and 1."
        )

    if not 0.0 <= health["px_efficiency"] <= 1.0:
        raise ValueError(
            "px_efficiency must be between 0 and 1."
        )

    if "zld" not in scenario:
        scenario["zld"] = {
            "enabled": True,
            "water_recovery": 0.90,
            "specific_energy": 20.0
        }

    zld = scenario["zld"]

    if not isinstance(zld, dict):
        raise ValueError(
            "Scenario section 'zld' must contain "
            "key-value pairs."
        )

    zld.setdefault(
        "enabled",
        True
    )

    zld.setdefault(
        "water_recovery",
        0.90
    )

    zld.setdefault(
        "specific_energy",
        20.0
    )

    if not isinstance(
        zld["enabled"],
        bool
    ):
        raise ValueError(
            "zld.enabled must be true or false."
        )

    if not (
        0.0
        <= zld["water_recovery"]
        <= 1.0
    ):
        raise ValueError(
            "zld.water_recovery must be "
            "between 0 and 1."
        )

    if zld["specific_energy"] < 0:
        raise ValueError(
            "zld.specific_energy cannot be negative."
        )

    return scenario