from __future__ import annotations

def clamp_score(score: float):
    """Clamp a score to [0, 1]."""
    return min(max(score, 0.0), 1.0)
