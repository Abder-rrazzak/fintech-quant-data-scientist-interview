"""Ranking, calibration, and operating-point metrics.

ROC-AUC answers "how well do we rank?". PR-AUC answers the same question when
positives are rare. Neither chooses a threshold. Thresholds are a cost decision.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def safe_roc_auc(y_true: np.ndarray, scores: np.ndarray) -> float | None:
    y_true = np.asarray(y_true).astype(int)
    if len(np.unique(y_true)) < 2:
        return None
    return float(roc_auc_score(y_true, scores))


def safe_pr_auc(y_true: np.ndarray, scores: np.ndarray) -> float | None:
    y_true = np.asarray(y_true).astype(int)
    if len(np.unique(y_true)) < 2:
        return None
    return float(average_precision_score(y_true, scores))


def brier_score(y_true: np.ndarray, probabilities: np.ndarray) -> float:
    return float(brier_score_loss(np.asarray(y_true).astype(int), np.asarray(probabilities, dtype=float)))


def ks_statistic(y_true: np.ndarray, scores: np.ndarray) -> float | None:
    """Kolmogorov-Smirnov distance between score CDFs of the two classes."""
    y_true = np.asarray(y_true).astype(int)
    scores = np.asarray(scores, dtype=float)
    if len(np.unique(y_true)) < 2:
        return None
    positive = np.sort(scores[y_true == 1])
    negative = np.sort(scores[y_true == 0])
    grid = np.unique(scores)
    cdf_pos = np.searchsorted(positive, grid, side="right") / max(len(positive), 1)
    cdf_neg = np.searchsorted(negative, grid, side="right") / max(len(negative), 1)
    return float(np.max(np.abs(cdf_pos - cdf_neg)))


def binary_at_threshold(y_true: np.ndarray, scores: np.ndarray, threshold: float) -> dict[str, float]:
    y_true = np.asarray(y_true).astype(int)
    pred = (np.asarray(scores, dtype=float) >= threshold).astype(int)
    tp = int(((pred == 1) & (y_true == 1)).sum())
    fp = int(((pred == 1) & (y_true == 0)).sum())
    tn = int(((pred == 0) & (y_true == 0)).sum())
    fn = int(((pred == 0) & (y_true == 1)).sum())
    return {
        "threshold": float(threshold),
        "precision": float(precision_score(y_true, pred, zero_division=0)),
        "recall": float(recall_score(y_true, pred, zero_division=0)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
    }


def recall_at_precision(
    y_true: np.ndarray, scores: np.ndarray, target_precision: float
) -> float | None:
    """Largest recall whose precision is still at least ``target_precision``."""
    y_true = np.asarray(y_true).astype(int)
    scores = np.asarray(scores, dtype=float)
    total_pos = int(y_true.sum())
    if total_pos == 0:
        return None
    order = np.argsort(-scores, kind="mergesort")
    y = y_true[order]
    tp = 0
    fp = 0
    best: float | None = None
    for label in y:
        if label == 1:
            tp += 1
        else:
            fp += 1
        precision = tp / (tp + fp)
        recall = tp / total_pos
        if precision + 1e-12 >= target_precision:
            best = recall
    return None if best is None else float(best)


def precision_at_recall(
    y_true: np.ndarray, scores: np.ndarray, target_recall: float
) -> float | None:
    """Precision at the smallest alert set that reaches ``target_recall``."""
    y_true = np.asarray(y_true).astype(int)
    scores = np.asarray(scores, dtype=float)
    total_pos = int(y_true.sum())
    if total_pos == 0:
        return None
    order = np.argsort(-scores, kind="mergesort")
    y = y_true[order]
    tp = 0
    fp = 0
    for label in y:
        if label == 1:
            tp += 1
        else:
            fp += 1
        recall = tp / total_pos
        if recall + 1e-12 >= target_recall:
            return float(tp / (tp + fp))
    return None


def classification_bundle(
    y_true: np.ndarray, scores: np.ndarray, threshold: float
) -> dict[str, float | None]:
    """Metrics a risk or fraud interviewer expects on one labeled window."""
    point = binary_at_threshold(y_true, scores, threshold)
    return {
        "roc_auc": safe_roc_auc(y_true, scores),
        "pr_auc": safe_pr_auc(y_true, scores),
        "ks": ks_statistic(y_true, scores),
        "brier": brier_score(y_true, np.clip(scores, 0.0, 1.0)),
        "recall_at_precision_30": recall_at_precision(y_true, scores, 0.30),
        "precision_at_recall_50": precision_at_recall(y_true, scores, 0.50),
        **point,
    }
