"""Expected loss for a simple unsecured loan laboratory.

Expected loss = PD x LGD x EAD.

This is a teaching identity. It is not a Basel capital calculator, and the
parameters here are synthetic assumptions, not estimated downturn LGDs.
"""

from __future__ import annotations

import numpy as np


def expected_loss(
    probability_of_default: np.ndarray | float,
    loss_given_default: np.ndarray | float,
    exposure_at_default: np.ndarray | float,
) -> np.ndarray | float:
    """Return PD x LGD x EAD, broadcasting the inputs."""
    pd_ = np.asarray(probability_of_default, dtype=float)
    lgd = np.asarray(loss_given_default, dtype=float)
    ead = np.asarray(exposure_at_default, dtype=float)
    if np.any((pd_ < 0) | (pd_ > 1)):
        raise ValueError("Probability of default must be between 0 and 1.")
    if np.any((lgd < 0) | (lgd > 1)):
        raise ValueError("Loss given default must be between 0 and 1.")
    if np.any(ead < 0):
        raise ValueError("Exposure at default must be non-negative.")
    loss = pd_ * lgd * ead
    if np.isscalar(probability_of_default) and np.isscalar(loss_given_default) and np.isscalar(
        exposure_at_default
    ):
        return float(loss)
    return loss


def portfolio_expected_loss(frame_pd, frame_lgd, frame_ead) -> float:
    """Sum of facility-level expected loss."""
    return float(np.sum(expected_loss(frame_pd, frame_lgd, frame_ead)))
