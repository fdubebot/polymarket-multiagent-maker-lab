import random
from dataclasses import dataclass

from pm_maker_lab.ai.linucb import LinUCBPolicy
from pm_maker_lab.core.orderbook import OrderBook
from pm_maker_lab.execution.network import NetworkModel
from pm_maker_lab.risk.limits import RiskLimits
from pm_maker_lab.strategy.fair_value import MarketContext, fair_value, make_quotes


@dataclass
class SimResult:
    steps: int
    fills: int
    drops: int
    avg_latency_ms: float
    inventory: int
    pnl_proxy: float


class MarketMakerSim:
    def __init__(self, seed: int = 7):
        self.rng = random.Random(seed)
        self.book = OrderBook(0.49, 0.51)
        self.net = NetworkModel()
        self.risk = RiskLimits()
        self.policy = LinUCBPolicy(n_features=3, alphas=[0.4, 0.7, 1.0])
        self.inventory = 0
        self.cash = 0.0

    def _sample_context(self) -> MarketContext:
        imbalance = self.rng.uniform(-1.0, 1.0)
        vol = self.rng.uniform(0.0, 1.0)
        implied = self.book.mid() + self.rng.uniform(-0.01, 0.01)
        return MarketContext(implied_prob=max(0.001, min(0.999, implied)), order_imbalance=imbalance, vol_regime=vol)

    def run(self, steps: int = 4000) -> SimResult:
        fills = 0
        drops = 0
        latencies = []

        for _ in range(steps):
            self.book.update_micro_move(self.rng.choice([-1, 0, 1]))
            ctx = self._sample_context()
            x = [ctx.implied_prob, ctx.order_imbalance, ctx.vol_regime]
            arm = self.policy.choose(x)
            aggression = [0.4, 0.7, 1.0][arm]

            fv = fair_value(ctx)
            bid, ask = make_quotes(fv, base_half_spread=0.012, aggression=aggression)
            ok, latency = self.net.transmit(self.rng)
            latencies.append(latency)
            if not ok:
                drops += 1
                continue

            side = self.rng.choice(["buy", "sell"])
            filled = (side == "buy" and bid >= self.book.best_bid) or (side == "sell" and ask <= self.book.best_ask)

            reward = -0.002
            if filled and self.risk.approve(self.inventory, self.book.mid(), 1):
                fills += 1
                if side == "buy":
                    self.inventory += 1
                    self.cash -= bid
                else:
                    self.inventory -= 1
                    self.cash += ask
                reward = 0.01 - 0.003 * abs(self.inventory)

            self.policy.update(arm, x, reward)

        pnl_proxy = self.cash + self.inventory * self.book.mid()
        return SimResult(
            steps=steps,
            fills=fills,
            drops=drops,
            avg_latency_ms=(sum(latencies) / len(latencies) if latencies else 0.0),
            inventory=self.inventory,
            pnl_proxy=pnl_proxy,
        )
