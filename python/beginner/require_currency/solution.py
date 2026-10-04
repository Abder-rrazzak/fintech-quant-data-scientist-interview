from __future__ import annotations

def require_currency(code: str):
    """Reject unknown currencies."""
    if code not in {'USD', 'EUR', 'GBP'}:
        raise ValueError(code)
    return code
