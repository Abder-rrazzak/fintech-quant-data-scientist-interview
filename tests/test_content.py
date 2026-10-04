"""Counts and small contracts that keep the laboratory from silently shrinking."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_question_bank_covers_required_topics() -> None:
    bank = json.loads((ROOT / "mock-interviews" / "question_bank.json").read_text(encoding="utf-8"))
    counts: dict[str, int] = {}
    for item in bank:
        counts[item["topic"]] = counts.get(item["topic"], 0) + 1
        for key in ("answer_30s", "answer_2min", "deep_dive", "common_mistake"):
            assert item[key]
        assert item["follow_ups"]
    minimums = {
        "python": 40,
        "sql": 100,
        "statistics": 100,
        "machine_learning": 30,
        "predictive_modeling": 30,
        "fraud": 30,
        "anomaly": 20,
        "credit_risk": 20,
        "clv": 15,
        "pandas": 50,
        "numpy": 30,
        "time_series": 30,
        "backtesting": 20,
        "spark": 30,
        "snowflake": 30,
        "aws": 30,
        "validation": 30,
        "bias": 20,
        "business": 30,
        "system_design": 30,
        "behavioral": 12,
    }
    missing = {topic: (counts.get(topic, 0), need) for topic, need in minimums.items() if counts.get(topic, 0) < need}
    assert not missing


def test_exercise_counts() -> None:
    python_solutions = list((ROOT / "python").rglob("solution.py"))
    sql_files = list((ROOT / "sql").rglob("*.sql"))
    assert len(python_solutions) >= 150
    assert len(sql_files) >= 200
    assert len(list((ROOT / "case-studies").glob("case_*.md"))) >= 30
    assert len(list((ROOT / "system-design").glob("design_*.md"))) >= 30
    assert len(list((ROOT / "case-studies" / "business-communication").glob("example_*.md"))) >= 30


def test_platt_is_monotonic() -> None:
    from evaluation.calibration import apply_platt, fit_platt

    scores = np.array([0.1, 0.2, 0.3, 0.8, 0.9, 0.05, 0.15, 0.85, 0.4, 0.6] * 3)
    labels = np.array([0, 0, 0, 1, 1, 0, 0, 1, 0, 1] * 3)
    model = fit_platt(scores, labels)
    mapped = apply_platt(model, np.array([0.2, 0.8]))
    assert mapped[1] > mapped[0]


def test_daily_spend_and_leakage_helper() -> None:
    from spark.job import customer_daily_spend

    frame = pd.DataFrame(
        {
            "transaction_id": ["a", "b", "c"],
            "customer_id": ["c1", "c1", "c2"],
            "timestamp": ["2024-01-01 01:00", "2024-01-01 02:00", "2024-01-02 01:00"],
            "amount": [10.0, 15.0, 7.0],
        }
    )
    daily = customer_daily_spend(frame)
    c1 = daily[daily["customer_id"] == "c1"].iloc[0]
    assert c1["spend"] == 25.0
    assert int(c1["txn_count"]) == 2
    leakage = _load(ROOT / "machine-learning" / "validation" / "leakage_examples.py", "leakage_examples")
    banned = leakage.columns_that_must_not_be_features()
    assert "is_fraud" in banned
    assert "utilization" not in banned
