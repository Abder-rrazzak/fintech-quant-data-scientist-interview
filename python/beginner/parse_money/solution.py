from __future__ import annotations

def parse_money(text: str):
    """Parse a money string."""
    cleaned = text.strip().replace('$', '').replace(',', '')
    if not cleaned:
        raise ValueError('empty')
    return float(cleaned)
