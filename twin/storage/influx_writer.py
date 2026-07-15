from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta


class InfluxWriter:

    def __init__(self):

        self.client = InfluxDBClient(
            url="http://localhost:8086",
            token="L4LEly7RwIHA_UnZdtI0RjvbMDSKRe-if0UxfSMc_qcFNDVgnpS_YOh6-Z6M_yzsGZjAaN40MPWy6EenHj9UEg==",
            org="zld"
        )

        self.write_api = self.client.write_api(
            write_options=SYNCHRONOUS
        )

        self.bucket = "plant_metrics"

        # Start virtual simulation time
        self.sim_time = datetime.utcnow()

    def write_state(self, state):

        point = (
            Point("plant_metrics")

            # Give each point a unique timestamp
            .time(self.sim_time)

            .field(
                "pump_power",
                state.assets.pump_power
            )

            .field(
                "net_power",
                state.assets.net_power
            )

            .field(
                "ro_recovery",
                state.assets.ro_recovery
            )

            .field(
                "ro_fouling",
                state.health.ro_fouling
            )

            .field(
                "pump_wear",
                state.health.pump_wear
            )

            .field(
                "px_efficiency",
                state.assets.px_efficiency
            )

            .field(
                "energy_cost",
                state.economics.cumulative_energy_cost
            )

            .field(
                "px_savings",
                state.economics.cumulative_px_savings
            )

            .field(
                "net_operating_cost",
                state.economics.net_operating_cost
            )

            .field(
                "tick",
                state.simulation.tick
            )
        )

        self.write_api.write(
            bucket=self.bucket,
            org="zld",
            record=point
        )

        # Move simulation time forward by 1 second
        self.sim_time += timedelta(seconds=1)