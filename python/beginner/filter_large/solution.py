from __future__ import annotations

def filter_large(totals: dict[int, float], cutoff: float):
    """Keep large totals."""
    return {key: value for key, value in totals.items() if value > cutoff}
