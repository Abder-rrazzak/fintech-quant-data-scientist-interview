"""Generate a laptop sample, train, and evaluate."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config.settings import SETTINGS  # noqa: E402
from data.generate import GenerateConfig, generate_dataset, write_dataset  # noqa: E402
from pipelines.training import run_training  # noqa: E402
from utils.logging import configure_logging  # noqa: E402


def main() -> None:
    configure_logging()
    config = GenerateConfig(n_customers=2000, n_transactions=25_000, seed=42)
    tables = generate_dataset(config)
    write_dataset(tables, SETTINGS.data_raw, config)
    result = run_training(SETTINGS.data_raw, SETTINGS.artifacts)
    print(result["summary"])


if __name__ == "__main__":
    main()
