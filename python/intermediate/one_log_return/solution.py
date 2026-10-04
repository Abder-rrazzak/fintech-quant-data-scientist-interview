from __future__ import annotations

def one_log_return(price_prev: float, price_now: float):
    """One log return."""
    import math
    if price_prev <= 0 or price_now <= 0:
        raise ValueError('price')
    return math.log(price_now / price_prev)
