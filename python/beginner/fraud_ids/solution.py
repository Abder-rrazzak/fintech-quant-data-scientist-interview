from __future__ import annotations

def fraud_ids(ids: list[int], flags: list[int]):
    """Ids with a fraud flag."""
    return [ids[i] for i in range(len(ids)) if flags[i] == 1]
