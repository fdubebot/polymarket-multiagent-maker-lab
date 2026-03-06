# polymarket-multiagent-maker-lab

A research-grade Python lab for **Polymarket-style market making** under realistic network conditions.

## What it does

- Simulates event-driven order book dynamics and market order flow.
- Models **network latency, jitter, and packet loss** in the execution path.
- Uses a lightweight **AI policy (LinUCB contextual bandit)** to choose quoting aggressiveness.
- Enforces risk controls (inventory and notional caps).
- Produces run summaries with fill quality, PnL proxy, and policy decisions.

## Why this exists

Real-world prediction market making depends on microstructure, edge quality, and systems behavior.
This project combines **AI + trading + networking** in one reproducible lab.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q
python -m pm_maker_lab.sim.runner --steps 4000 --seed 7
```

## Project layout

- `src/pm_maker_lab/core/orderbook.py` - minimal LOB + spread/mid operations
- `src/pm_maker_lab/strategy/fair_value.py` - fair-value + quote generation
- `src/pm_maker_lab/ai/linucb.py` - contextual bandit for aggression selection
- `src/pm_maker_lab/execution/network.py` - latency/jitter/loss model
- `src/pm_maker_lab/risk/limits.py` - pre-trade risk gates
- `src/pm_maker_lab/sim/engine.py` - event simulation engine
- `src/pm_maker_lab/sim/runner.py` - CLI runner + report output

## Status

Prototype complete with tests; ready for:
- richer market data adapters
- multi-asset coupling
- calibration against historical Polymarket snapshots
