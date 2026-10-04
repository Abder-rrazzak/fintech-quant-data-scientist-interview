from __future__ import annotations

def month_over_month(previous: float | None, current: float):
    """Month-over-month change."""
    if previous is None or previous == 0:
        return None
    return (current - previous) / previous
