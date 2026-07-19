class SimulationClock:

    def __init__(
        self,
        dt_seconds=10.0
    ):
        self.dt_seconds = float(
            dt_seconds
        )

        if self.dt_seconds <= 0.0:
            raise ValueError(
                "Simulation time step must be "
                "greater than zero."
            )

        self.dt_hours = (
            self.dt_seconds
            / 3600.0
        )