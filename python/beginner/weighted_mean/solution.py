from __future__ import annotations

def weighted_mean(values: list[float], weights: list[float]):
    """Weighted mean."""
    if len(values) != len(weights) or not values:
        raise ValueError('shape')
    total_w = sum(weights)
    if total_w == 0:
        raise ValueError('weights')
    return sum(v * w for v, w in zip(values, weights)) / total_w
