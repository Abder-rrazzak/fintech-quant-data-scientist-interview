from __future__ import annotations

def zscore_list(values: list[float]):
    """Population z-score."""
    if not values:
        return []
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    if var == 0:
        return [0.0 for _ in values]
    std = var ** 0.5
    return [(v - mean) / std for v in values]
