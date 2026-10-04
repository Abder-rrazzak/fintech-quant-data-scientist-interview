from __future__ import annotations

def iso_month(timestamp: str):
    """Month key from an ISO timestamp."""
    if len(timestamp) < 7:
        raise ValueError('timestamp')
    return timestamp[:7]
