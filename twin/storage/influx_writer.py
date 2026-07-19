import os
from datetime import datetime, timedelta, timezone

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxWriter:

    def __init__(self):
        self.url = os.getenv(
            "INFLUXDB_URL",
            "http://localhost:8086"
        )

        self.token = os.getenv("INFLUXDB_TOKEN")

        self.org = os.getenv(
            "INFLUXDB_ORG",
            "zld"
        )

        self.bucket = os.getenv(
            "INFLUXDB_BUCKET",
            "plant_metrics"
        )

        self.client = None
        self.write_api = None

        self.enabled = False
        self.warning_shown = False

        self.sim_time = datetime.now(
            timezone.utc
        )

        if not self.token:
            print(
                "InfluxDB telemetry disabled: "
                "INFLUXDB_TOKEN is not configured."
            )
            return

        try:
            self.client = InfluxDBClient(
                url=self.url,
                token=self.token,
                org=self.org
            )

            self.write_api = self.client.write_api(
                write_options=SYNCHRONOUS
            )

            self.enabled = True

        except Exception as error:
            print(
                "InfluxDB initialization failed. "
                "Simulation will continue without telemetry."
            )

            print(f"Reason: {error}")

            self.enabled = False

    def write_state(self, state):
        if not self.enabled:
            self._advance_visual_time()
            return

        point = (
            Point("plant_metrics")

            .time(self.sim_time)

            .field("feed_flow", float(state.process.feed_flow))
            .field("feed_tds", float(state.process.feed_tds))
            .field("feed_temperature", float(state.process.feed_temperature))
            .field("operating_pressure", float(state.process.operating_pressure))

            .field("pump_pressure", float(state.assets.pump_pressure))
            .field("pump_power", float(state.assets.pump_power))
            .field("pump_efficiency", float(state.assets.pump_efficiency))
            .field("pump_wear", float(state.health.pump_wear))

            .field("ro_recovery", float(state.assets.ro_recovery))
            .field("ro_permeate_flow", float(state.assets.ro_permeate_flow))
            .field("ro_brine_flow", float(state.assets.ro_brine_flow))
            .field("permeate_tds", float(state.assets.permeate_tds))
            .field("brine_tds", float(state.assets.brine_tds))
            .field("ro_required_pressure", float(state.assets.ro_required_pressure))
            .field("ro_fouling", float(state.health.ro_fouling))

            .field("px_recovered_power", float(state.assets.px_recovered_power))
            .field("px_efficiency", float(state.assets.px_efficiency))
            .field("px_enabled", bool(state.assets.px_enabled))
            .field("net_power", float(state.assets.net_power))

            .field("brine_to_zld", float(state.assets.brine_to_zld))
            .field("zld_water_recovered", float(state.assets.zld_water_recovered))
            .field("zld_residual_liquid", float(state.assets.zld_residual_liquid))
            .field("zld_recovery", float(state.assets.zld_recovery))
            .field("zld_solid_residue", float(state.assets.zld_solid_residue))
            .field("zld_power", float(state.assets.zld_power))
            .field(
                "zld_energy_consumption",
                float(state.assets.zld_energy_consumption)
            )

            .field(
                "total_recovered_water",
                float(state.process.total_recovered_water)
            )

            .field(
                "overall_water_recovery",
                float(state.process.overall_water_recovery)
            )

            .field(
                "total_plant_power",
                float(state.assets.total_plant_power)
            )

            .field("energy_cost", float(state.economics.energy_cost))
            .field("ro_energy_cost", float(state.economics.ro_energy_cost))
            .field("zld_energy_cost", float(state.economics.zld_energy_cost))

            .field(
                "cumulative_energy_cost",
                float(state.economics.cumulative_energy_cost)
            )

            .field(
                "cumulative_ro_energy_cost",
                float(state.economics.cumulative_ro_energy_cost)
            )

            .field(
                "cumulative_zld_energy_cost",
                float(state.economics.cumulative_zld_energy_cost)
            )

            .field("px_savings", float(state.economics.px_savings))

            .field(
                "cumulative_px_savings",
                float(state.economics.cumulative_px_savings)
            )

            .field(
                "net_operating_cost",
                float(state.economics.net_operating_cost)
            )

            .field(
                "power_price",
                float(state.economics.power_price)
            )

            .field("tick", int(state.simulation.tick))
            .field(
                "runtime_hours",
                float(state.simulation.runtime_hours)
            )
        )

        try:
            self.write_api.write(
                bucket=self.bucket,
                org=self.org,
                record=point
            )

        except Exception as error:
            if not self.warning_shown:
                print(
                    "Warning: InfluxDB write failed. "
                    "Telemetry has been disabled, but the "
                    "simulation will continue."
                )

                print(f"Reason: {error}")

                self.warning_shown = True

            self.enabled = False

        self._advance_visual_time()

    def _advance_visual_time(self):
        self.sim_time += timedelta(
            seconds=1
        )

    def close(self):
        if self.write_api is not None:
            try:
                self.write_api.close()
            except Exception:
                pass

        if self.client is not None:
            try:
                self.client.close()
            except Exception:
                pass