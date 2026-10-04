from __future__ import annotations

def precision_recall(tp: int, fp: int, fn: int):
    """Precision and recall."""
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return (precision, recall)
