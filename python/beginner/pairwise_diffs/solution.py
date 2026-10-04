from __future__ import annotations

def pairwise_diffs(amounts: list[float]):
    """Consecutive amount changes."""
    return [amounts[i] - amounts[i - 1] for i in range(1, len(amounts))]
