from __future__ import annotations

def valid_currency(code: str):
    """Validate a currency code."""
    return code in {'USD', 'EUR', 'GBP'}
