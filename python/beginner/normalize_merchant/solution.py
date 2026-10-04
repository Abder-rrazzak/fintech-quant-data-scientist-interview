from __future__ import annotations

def normalize_merchant(name: str):
    """Normalize a merchant name."""
    return ' '.join(name.strip().lower().split())
