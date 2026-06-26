from dataclasses import dataclass

@dataclass
class ProcessState:
    feed_flow: float
    feed_tds: float
    feed_temperature: float

    permeate_flow: float = 0.0
    brine_flow: float = 0.0