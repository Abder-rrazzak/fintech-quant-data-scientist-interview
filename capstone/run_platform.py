"""Run the laboratory platform on a small synthetic book kept inside capstone/.

Snowflake and AWS are documented alternatives. This script uses local Parquet,
scikit-learn, and the files already in src/.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from data.generate import GenerateConfig, generate_dataset, write_dataset  # noqa: E402
from data.quality import quality_report  # noqa: E402
from pipelines.training import run_training  # noqa: E402
from utils.logging import configure_logging  # noqa: E402


def main() -> None:
    configure_logging()
    here = Path(__file__).resolve().parent
    raw = here / "data" / "raw"
    artifacts = here / "artifacts"
    config = GenerateConfig(n_customers=300, n_transactions=4000, seed=42)
    tables = generate_dataset(config)
    write_dataset(tables, raw, config)
    report = quality_report(tables["transactions"])
    training = run_training(raw, artifacts)
    (here / "run_notes.md").write_text(
        "\n".join(
            [
                "# Capstone run notes",
                "",
                "Synthetic book generated inside `capstone/data`. It is not a client dataset.",
                "",
                f"Rows: {report['rows']}. Fraud rate in the raw extract: {report['fraud_rate']:.4f}.",
                f"Duplicate transaction ids injected: {report['duplicate_transaction_ids']}.",
                "",
                training["summary"],
            ]
        ),
        encoding="utf-8",
    )
    print(training["summary"])


if __name__ == "__main__":
    main()
