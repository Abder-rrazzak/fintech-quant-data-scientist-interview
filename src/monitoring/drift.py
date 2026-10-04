"""Population stability index and simple drift comparisons.

PSI compares two distributions through bins defined on a reference sample.
A common rule of thumb is: below 0.10 little shift, 0.10 to 0.25 moderate,
above 0.25 large. Those cutoffs are conventions, not laws. Alert thresholds
belong to the operating team and should be calibrated on historical shifts
that actually changed a decision.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def population_stability_index(
    expected: np.ndarray, actual: np.ndarray, bins: int = 10
) -> float:
    """PSI of ``actual`` against bins cut on ``expected``."""
    expected = np.asarray(expected, dtype=float)
    actual = np.asarray(actual, dtype=float)
    expected = expected[np.isfinite(expected)]
    actual = actual[np.isfinite(actual)]
    if len(expected) < bins or len(actual) == 0:
        return float("nan")
    quantiles = np.linspace(0, 1, bins + 1)
    breaks = np.unique(np.quantile(expected, quantiles))
    if len(breaks) < 3:
        return 0.0
    breaks[0] = -np.inf
    breaks[-1] = np.inf
    expected_counts = np.histogram(expected, bins=breaks)[0].astype(float)
    actual_counts = np.histogram(actual, bins=breaks)[0].astype(float)
    expected_pct = np.clip(expected_counts / expected_counts.sum(), 1e-6, None)
    actual_pct = np.clip(actual_counts / actual_counts.sum(), 1e-6, None)
    return float(np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct)))


def psi_table(
    reference: pd.DataFrame, current: pd.DataFrame, columns: list[str], bins: int = 10
) -> pd.DataFrame:
    rows = []
    for column in columns:
        rows.append(
            {
                "feature": column,
                "psi": population_stability_index(
                    reference[column].to_numpy(), current[column].to_numpy(), bins=bins
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("psi", ascending=False)


def alert(psi: float, moderate: float = 0.10, large: float = 0.25) -> str:
    if psi != psi:
        return "insufficient_data"
    if psi < moderate:
        return "ok"
    if psi < large:
        return "moderate"
    return "large"
