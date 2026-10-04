from __future__ import annotations

def simple_clv_identity(aov: float, purchases: float, margin: float, lifespan: float):
    """Historical CLV."""
    if min(purchases, margin, lifespan) < 0:
        raise ValueError('negative')
    return aov * purchases * margin * lifespan
