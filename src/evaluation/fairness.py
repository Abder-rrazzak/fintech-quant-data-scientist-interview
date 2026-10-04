"""Statistical disparity diagnostics.

These functions measure differences in selection or error rates across groups.
They are not a legal conclusion. Whether a disparity is unlawful depends on
jurisdiction, the decision context, and facts this laboratory does not have.
Do not describe a metric gap as proof of illegal discrimination.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _rates_by_group(mask: np.ndarray, groups: np.ndarray) -> pd.Series:
    frame = pd.DataFrame({"group": groups, "flag": mask.astype(float)})
    return frame.groupby("group", sort=True)["flag"].mean()


def approval_rates(y_pred: np.ndarray, groups: np.ndarray) -> pd.Series:
    """Share predicted positive (approved, or flagged) in each group."""
    return _rates_by_group(np.asarray(y_pred).astype(bool), np.asarray(groups))


def demographic_parity_difference(y_pred: np.ndarray, groups: np.ndarray) -> float:
    """Max group selection rate minus min group selection rate."""
    rates = approval_rates(y_pred, groups)
    if rates.empty:
        return 0.0
    return float(rates.max() - rates.min())


def true_positive_rates(y_true: np.ndarray, y_pred: np.ndarray, groups: np.ndarray) -> pd.Series:
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    groups = np.asarray(groups)
    rows = []
    for group in pd.unique(groups):
        subset = groups == group
        positives = y_true[subset] == 1
        if positives.sum() == 0:
            rate = np.nan
        else:
            rate = float(((y_pred[subset] == 1) & positives).sum() / positives.sum())
        rows.append((group, rate))
    return pd.Series({group: rate for group, rate in rows}).sort_index()


def equal_opportunity_difference(
    y_true: np.ndarray, y_pred: np.ndarray, groups: np.ndarray
) -> float:
    """Absolute gap between the highest and lowest true positive rates."""
    rates = true_positive_rates(y_true, y_pred, groups).dropna()
    if rates.empty:
        return 0.0
    return float(rates.max() - rates.min())


def performance_by_group(
    y_true: np.ndarray, y_pred: np.ndarray, groups: np.ndarray
) -> pd.DataFrame:
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    groups = np.asarray(groups)
    records = []
    for group in sorted(pd.unique(groups), key=str):
        subset = groups == group
        yt = y_true[subset]
        yp = y_pred[subset]
        tp = int(((yp == 1) & (yt == 1)).sum())
        fp = int(((yp == 1) & (yt == 0)).sum())
        fn = int(((yp == 0) & (yt == 1)).sum())
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        records.append(
            {
                "group": group,
                "n": int(subset.sum()),
                "selection_rate": float(yp.mean()) if len(yp) else 0.0,
                "precision": precision,
                "recall": recall,
            }
        )
    return pd.DataFrame(records)
