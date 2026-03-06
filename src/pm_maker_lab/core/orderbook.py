from dataclasses import dataclass


@dataclass
class OrderBook:
    best_bid: float
    best_ask: float

    def mid(self) -> float:
        return (self.best_bid + self.best_ask) / 2.0

    def spread(self) -> float:
        return max(0.0, self.best_ask - self.best_bid)

    def update_micro_move(self, signed_ticks: int, tick_size: float = 0.001) -> None:
        move = signed_ticks * tick_size
        self.best_bid = max(0.001, min(0.999, self.best_bid + move))
        self.best_ask = max(self.best_bid + tick_size, min(0.999, self.best_ask + move))
