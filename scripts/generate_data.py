"""Generate the synthetic financial laboratory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from data.generate import GenerateConfig, generate_dataset, write_dataset  # noqa: E402
from utils.logging import configure_logging  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic financial laboratory data.")
    parser.add_argument("--customers", type=int, default=10_000)
    parser.add_argument("--transactions", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "raw")
    args = parser.parse_args()
    configure_logging()
    config = GenerateConfig(
        n_customers=args.customers,
        n_transactions=args.transactions,
        seed=args.seed,
    )
    tables = generate_dataset(config)
    write_dataset(tables, args.output, config)


if __name__ == "__main__":
    main()
