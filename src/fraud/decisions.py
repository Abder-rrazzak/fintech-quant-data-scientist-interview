"""Approve, review, or block from two thresholds.

A single cutoff hides the operational difference between a quiet review queue
and an automatic block. Two thresholds make that queue explicit.
"""

from __future__ import annotations

import numpy as np


def decide(scores: np.ndarray, review_threshold: float, block_threshold: float) -> np.ndarray:
    """Map scores to approve / review / block.

    ``block_threshold`` must be greater than or equal to ``review_threshold``.
    """
    if block_threshold < review_threshold:
        raise ValueError("Block threshold must be at least the review threshold.")
    scores = np.asarray(scores, dtype=float)
    decisions = np.full(len(scores), "approve", dtype=object)
    decisions[scores >= review_threshold] = "review"
    decisions[scores >= block_threshold] = "block"
    return decisions
