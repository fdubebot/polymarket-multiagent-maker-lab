from dataclasses import dataclass


@dataclass
class MarketContext:
    implied_prob: float
    order_imbalance: float
    vol_regime: float


def fair_value(ctx: MarketContext, alpha_weight: float = 0.08) -> float:
    raw = ctx.implied_prob + alpha_weight * ctx.order_imbalance
    damped = raw * (1.0 - 0.2 * min(1.0, ctx.vol_regime))
    return max(0.001, min(0.999, damped))


def make_quotes(fv: float, base_half_spread: float, aggression: float) -> tuple[float, float]:
    # higher aggression => tighter spread
    half = max(0.001, base_half_spread * (1.2 - aggression))
    bid = max(0.001, fv - half)
    ask = min(0.999, fv + half)
    if ask <= bid:
        ask = min(0.999, bid + 0.001)
    return bid, ask
