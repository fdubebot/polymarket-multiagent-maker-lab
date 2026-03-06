from pm_maker_lab.sim.engine import MarketMakerSim


def test_sim_runs():
    sim = MarketMakerSim(seed=42)
    res = sim.run(steps=300)
    assert res.steps == 300
    assert res.avg_latency_ms > 0
