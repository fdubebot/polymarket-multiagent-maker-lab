import random

from pm_maker_lab.execution.network import NetworkModel


def test_network_transmit_ranges():
    n = NetworkModel(base_latency_ms=20, jitter_ms=5, drop_prob=0.0)
    ok, latency = n.transmit(random.Random(1))
    assert ok is True
    assert latency >= 1.0
