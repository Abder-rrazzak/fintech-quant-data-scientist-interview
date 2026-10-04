from __future__ import annotations

def moving_sum(amounts: list[float], k: int):
    """Moving sum."""
    if k <= 0:
        raise ValueError('k')
    if k > len(amounts):
        return []
    window = sum(amounts[:k])
    out = [window]
    for i in range(k, len(amounts)):
        window += amounts[i] - amounts[i - k]
        out.append(window)
    return out
