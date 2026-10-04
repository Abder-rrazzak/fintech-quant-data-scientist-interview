"""Choose an operating point from business cost, not from accuracy."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def threshold_cost_curve(
    y_true: np.ndarray,
    scores: np.ndarray,
    fn_cost: float = 500.0,
    fp_cost: float = 5.0,
    thresholds: np.ndarray | None = None,
) -> pd.DataFrame:
    """Expected cost = FN * fn_cost + FP * fp_cost, ignoring investigation overhead.

    True positives are treated as paid for by the investigation process already
    counted, in part, through the false-positive cost of reviews. Extend the
    cost model if investigators have a separate unit cost.
    """
    y_true = np.asarray(y_true).astype(int)
    scores = np.asarray(scores, dtype=float)
    if thresholds is None:
        thresholds = np.round(np.linspace(0.01, 0.99, 99), 4)
    rows: list[dict[str, float]] = []
    n = max(len(y_true), 1)
    for threshold in thresholds:
        pred = scores >= threshold
        fp = int((pred & (y_true == 0)).sum())
        fn = int((~pred & (y_true == 1)).sum())
        tp = int((pred & (y_true == 1)).sum())
        tn = int((~pred & (y_true == 0)).sum())
        rows.append(
            {
                "threshold": float(threshold),
                "false_positives": fp,
                "false_negatives": fn,
                "true_positives": tp,
                "true_negatives": tn,
                "business_cost": float(fp * fp_cost + fn * fn_cost),
                "flag_rate": float(pred.mean()) if n else 0.0,
            }
        )
    return pd.DataFrame(rows)


def select_threshold(curve: pd.DataFrame) -> pd.Series:
    """Return the lowest-cost row. Ties break toward the higher threshold."""
    if curve.empty:
        raise ValueError("Cost curve is empty.")
    ordered = curve.sort_values(["business_cost", "threshold"], ascending=[True, False])
    return ordered.iloc[0]


def plot_cost_curve(curve: pd.DataFrame, path: Path, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axis = plt.subplots(figsize=(8, 4.5))
    axis.plot(curve["threshold"], curve["business_cost"], label="Business cost", color="#0f3d5e")
    axis.set_xlabel("Threshold")
    axis.set_ylabel("False-positive cost + false-negative cost")
    axis.set_title(title)
    twin = axis.twinx()
    twin.plot(curve["threshold"], curve["false_positives"], color="#c47b2b", alpha=0.8, label="FP")
    twin.plot(curve["threshold"], curve["false_negatives"], color="#8c2f39", alpha=0.8, label="FN")
    twin.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
