from pm_maker_lab.strategy.fair_value import MarketContext, fair_value, make_quotes


def test_fair_value_bounds_and_quotes():
    ctx = MarketContext(implied_prob=0.98, order_imbalance=1.0, vol_regime=0.9)
    fv = fair_value(ctx)
    bid, ask = make_quotes(fv, base_half_spread=0.01, aggression=0.8)
    assert 0.001 <= fv <= 0.999
    assert bid < ask
