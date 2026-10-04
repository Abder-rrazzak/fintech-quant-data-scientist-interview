from __future__ import annotations

def count_calls(func):
    """Count calls."""
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper
