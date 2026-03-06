from pm_maker_lab.core.orderbook import OrderBook


def test_mid_spread():
    ob = OrderBook(0.4, 0.6)
    assert ob.mid() == 0.5
    assert abs(ob.spread() - 0.2) < 1e-9
