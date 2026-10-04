from __future__ import annotations

def net_return(gross: float, turnover: float, cost_bps: float):
    """Return after transaction cost."""
    return gross - turnover * cost_bps / 10000.0
