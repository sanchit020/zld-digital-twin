class SimulationClock:

    def __init__(self, dt_seconds=10):

        self.dt_seconds = dt_seconds

    @property
    def dt_hours(self):

        return self.dt_seconds / 3600.0