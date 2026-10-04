from __future__ import annotations

def rolling_mean_py(values: list[float], k: int):
    """Rolling mean."""
    if k <= 0:
        raise ValueError('k')
    out = []
    for i in range(len(values)):
        if i + 1 < k:
            out.append(None)
        else:
            window = values[i + 1 - k:i + 1]
            out.append(sum(window) / k)
    return out
