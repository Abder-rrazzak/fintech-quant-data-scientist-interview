from __future__ import annotations

def brier_score(y_true: list[int], probs: list[float]):
    """Brier score."""
    if len(y_true) != len(probs) or not y_true:
        raise ValueError('shape')
    return sum((probs[i] - y_true[i]) ** 2 for i in range(len(y_true))) / len(y_true)
