from __future__ import annotations

def top_k_amounts(amounts: list[float], k: int):
    """Top k amounts."""
    if k < 0:
        raise ValueError('k')
    return sorted(amounts, reverse=True)[:k]
