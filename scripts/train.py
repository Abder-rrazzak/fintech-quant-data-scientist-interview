"""Train fraud and credit models on the synthetic laboratory."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config.settings import SETTINGS  # noqa: E402
from pipelines.training import run_training  # noqa: E402
from utils.logging import configure_logging  # noqa: E402


def main() -> None:
    configure_logging()
    raw = SETTINGS.data_raw
    if not (raw / "transactions.parquet").exists():
        raise SystemExit(
            "No data/raw/transactions.parquet. Run scripts/generate_data.py first."
        )
    result = run_training(raw, SETTINGS.artifacts)
    print(result["summary"])


if __name__ == "__main__":
    main()
