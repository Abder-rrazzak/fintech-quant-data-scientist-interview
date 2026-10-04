from __future__ import annotations

def fraud_decision(score: float, review_threshold: float, block_threshold: float):
    """Approve, review, or block."""
    if block_threshold < review_threshold:
        raise ValueError('thresholds')
    if score >= block_threshold:
        return 'block'
    if score >= review_threshold:
        return 'review'
    return 'approve'
