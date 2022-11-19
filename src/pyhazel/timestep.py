__all__ = ["Timestep"]


class Timestep:
    def __init__(self, time=0) -> None:
        self.time = time

    @property
    def seconds(self):
        return self.time

    @property
    def milli_seconds(self):
        return self.time * 1000
