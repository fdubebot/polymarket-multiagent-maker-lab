import random
from dataclasses import dataclass


@dataclass
class NetworkModel:
    base_latency_ms: float = 35.0
    jitter_ms: float = 12.0
    drop_prob: float = 0.02

    def transmit(self, rng: random.Random) -> tuple[bool, float]:
        dropped = rng.random() < self.drop_prob
        latency = max(1.0, self.base_latency_ms + rng.uniform(-self.jitter_ms, self.jitter_ms))
        return (not dropped), latency
