from __future__ import annotations

def flatten_batches(batches: list[list[int]]):
    """Flatten batches."""
    return [item for batch in batches for item in batch]
