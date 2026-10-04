from __future__ import annotations

def cost_at_threshold(y_true: list[int], scores: list[float], threshold: float, fp_cost: float, fn_cost: float):
    """Cost at a threshold."""
    fp = fn = 0
    for truth, score in zip(y_true, scores):
        pred = score >= threshold
        if pred and truth == 0:
            fp += 1
        if (not pred) and truth == 1:
            fn += 1
    return fp * fp_cost + fn * fn_cost
