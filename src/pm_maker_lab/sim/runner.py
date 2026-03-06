import argparse

from pm_maker_lab.sim.engine import MarketMakerSim


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Polymarket market-maker lab simulation")
    parser.add_argument("--steps", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    sim = MarketMakerSim(seed=args.seed)
    result = sim.run(steps=args.steps)

    print("=== polymarket-multiagent-maker-lab report ===")
    print(f"steps: {result.steps}")
    print(f"fills: {result.fills}")
    print(f"drops: {result.drops}")
    print(f"avg_latency_ms: {result.avg_latency_ms:.2f}")
    print(f"inventory: {result.inventory}")
    print(f"pnl_proxy: {result.pnl_proxy:.6f}")


if __name__ == "__main__":
    main()
