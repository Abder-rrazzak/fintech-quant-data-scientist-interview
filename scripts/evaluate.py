"""Print the saved business evaluation. Does not refit models."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config.settings import SETTINGS  # noqa: E402


def main() -> None:
    summary = SETTINGS.artifacts / "evaluation_summary.md"
    report = SETTINGS.artifacts / "monitoring_report.md"
    if not summary.exists():
        raise SystemExit("No evaluation summary. Run scripts/train.py first.")
    print(summary.read_text(encoding="utf-8"))
    if report.exists():
        print(report.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
