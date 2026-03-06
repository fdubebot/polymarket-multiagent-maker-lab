from pm_maker_lab.ai.linucb import LinUCBPolicy


def test_linucb_choose_update():
    p = LinUCBPolicy(n_features=3, alphas=[0.4, 0.7, 1.0])
    x = [0.5, -0.2, 0.3]
    arm = p.choose(x)
    p.update(arm, x, reward=0.2)
    arm2 = p.choose(x)
    assert 0 <= arm2 < 3
