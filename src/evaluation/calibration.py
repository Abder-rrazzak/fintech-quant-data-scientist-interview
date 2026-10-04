"""Platt scaling for laboratory probabilities.

The mapping is fit on training scores only. The validation window is reserved
for the threshold. This is a teaching calibration, not a regulatory one.
"""

from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression


def fit_platt(scores: np.ndarray, labels: np.ndarray) -> LogisticRegression | None:
    """Fit a one-dimensional logistic map from score to probability."""
    y = np.asarray(labels, dtype=int)
    x = np.asarray(scores, dtype=float).reshape(-1, 1)
    if len(y) < 20 or len(np.unique(y)) < 2:
        return None
    model = LogisticRegression(max_iter=200)
    model.fit(x, y)
    return model


def apply_platt(model: LogisticRegression | None, scores: np.ndarray) -> np.ndarray:
    """Apply a fitted map. A missing map returns the scores unchanged."""
    raw = np.asarray(scores, dtype=float)
    if model is None:
        return raw
    return model.predict_proba(raw.reshape(-1, 1))[:, 1]
