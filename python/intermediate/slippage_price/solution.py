from __future__ import annotations

def slippage_price(price: float, side: str, slippage_bps: float):
    """Slippage-adjusted price."""
    bump = slippage_bps / 10000.0
    if side == 'buy':
        return price * (1 + bump)
    if side == 'sell':
        return price * (1 - bump)
    raise ValueError(side)
