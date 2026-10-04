from __future__ import annotations

def causal_split_ok(train_end: int, test_start: int):
    """Causal split check."""
    return train_end <= test_start
