from __future__ import annotations

def amount_lookup(ids: list[int], amounts: list[float]):
    """Map ids to amounts."""
    if len(ids) != len(amounts):
        raise ValueError('length')
    return {ids[i]: amounts[i] for i in range(len(ids))}
