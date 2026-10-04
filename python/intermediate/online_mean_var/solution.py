from __future__ import annotations

def online_mean_var(values: list[float]):
    """Welford mean and variance."""
    if not values:
        raise ValueError('empty')
    mean = 0.0
    m2 = 0.0
    for i, value in enumerate(values, start=1):
        delta = value - mean
        mean += delta / i
        m2 += delta * (value - mean)
    return mean, m2 / len(values)
