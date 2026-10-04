from __future__ import annotations

def high_risk_mcc(category: str):
    """High-risk category."""
    return int(category in {'gambling', 'crypto', 'wire', 'luxury'})
