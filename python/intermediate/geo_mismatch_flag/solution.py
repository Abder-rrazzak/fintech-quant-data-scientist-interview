from __future__ import annotations

def geo_mismatch_flag(home: str | None, country: str | None):
    """Country mismatch."""
    if not home or not country:
        return 0
    return int(home != country)
