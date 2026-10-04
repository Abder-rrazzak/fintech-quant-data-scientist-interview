from __future__ import annotations

def expected_loss_identity(pd: float, lgd: float, ead: float):
    """Expected loss."""
    if not 0 <= pd <= 1 or not 0 <= lgd <= 1 or ead < 0:
        raise ValueError('inputs')
    return pd * lgd * ead
