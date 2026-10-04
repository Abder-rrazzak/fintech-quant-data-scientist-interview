from __future__ import annotations

def prior_mean_list(values: list[float]):
    """Prior mean."""
    out = []
    total = 0.0
    for i, value in enumerate(values):
        out.append(None if i == 0 else total / i)
        total += value
    return out
