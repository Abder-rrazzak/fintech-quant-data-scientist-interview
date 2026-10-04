"""Slice approval and true-positive rates. This is a measurement, not a legal finding."""

from __future__ import annotations

import numpy as np
import pandas as pd

from evaluation.fairness import demographic_parity_difference, equal_opportunity_difference


def approval_table(frame: pd.DataFrame, group_col: str, score_col: str, label_col: str, threshold: float) -> pd.DataFrame:
    work = frame.copy()
    work["approved"] = (work[score_col] < threshold).astype(int)
    rows = []
    for name, part in work.groupby(group_col):
        rows.append(
            {
                "group": name,
                "n": int(len(part)),
                "approval_rate": float(part["approved"].mean()),
                "default_rate": float(part[label_col].mean()),
            }
        )
    return pd.DataFrame(rows)


def gaps(y: np.ndarray, approved: np.ndarray, group: np.ndarray) -> dict[str, float]:
    return {
        "demographic_parity_difference": demographic_parity_difference(approved, group),
        "equal_opportunity_difference": equal_opportunity_difference(y, approved, group),
    }
