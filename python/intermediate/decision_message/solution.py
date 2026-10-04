from __future__ import annotations

def decision_message(decision: str, score: float):
    """Decision log line."""
    return f'decision={decision} score={score:.3f}'
