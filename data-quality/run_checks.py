"""Write a data-quality report for a transaction extract."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from data.quality import quality_report, validate_transactions


def run(path: Path, output: Path) -> dict:
    frame = pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path)
    report = quality_report(frame)
    report["issues"] = validate_transactions(frame)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
