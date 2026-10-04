from __future__ import annotations

def missing_columns(header: list[str], required: list[str]):
    """Missing required columns."""
    have = set(header)
    return sorted(name for name in required if name not in have)
