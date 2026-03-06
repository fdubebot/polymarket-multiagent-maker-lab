from pm_maker_lab.risk.limits import RiskLimits


def test_risk_approve():
    r = RiskLimits(max_inventory=2, max_notional=1.0)
    assert r.approve(inventory=0, quote_mid=0.4, order_size=1)
    assert not r.approve(inventory=2, quote_mid=0.4, order_size=1)
