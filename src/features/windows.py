"""Point-in-time window statistics on arrays sorted by entity then time.

These routines include the current row in counts and sums. Amount z-scores
compare the current amount with the history that excludes the current row.
"""

from __future__ import annotations

import numpy as np


def window_count_and_sum(
    entity_ids: np.ndarray,
    timestamps_ns: np.ndarray,
    amounts: np.ndarray,
    window_ns: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Count and sum amounts inside ``(t - window, t]`` for each row.

    Parameters
    ----------
    entity_ids, timestamps_ns, amounts:
        Equal-length arrays sorted by entity id, then timestamp.
    window_ns:
        Window length in nanoseconds. The current row is included.
    """
    n = len(entity_ids)
    counts = np.zeros(n, dtype=np.int32)
    sums = np.zeros(n, dtype=np.float64)
    if n == 0:
        return counts, sums
    left = 0
    running = 0.0
    timestamps_ns = np.asarray(timestamps_ns, dtype=np.int64)
    amounts = np.asarray(amounts, dtype=np.float64)
    for i in range(n):
        if i > 0 and entity_ids[i] != entity_ids[i - 1]:
            left = i
            running = 0.0
        running += amounts[i]
        limit = timestamps_ns[i] - np.int64(window_ns)
        while timestamps_ns[left] < limit:
            running -= amounts[left]
            left += 1
        counts[i] = i - left + 1
        sums[i] = running
    return counts, sums


def prior_mean_and_std(entity_ids: np.ndarray, amounts: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Expanding mean and population std of rows strictly before the current row."""
    n = len(entity_ids)
    means = np.full(n, np.nan, dtype=np.float64)
    stds = np.full(n, np.nan, dtype=np.float64)
    amounts = np.asarray(amounts, dtype=np.float64)
    count = 0
    total = 0.0
    total_sq = 0.0
    for i in range(n):
        if i == 0 or entity_ids[i] != entity_ids[i - 1]:
            count = 0
            total = 0.0
            total_sq = 0.0
        if count > 0:
            mean = total / count
            means[i] = mean
            if count > 1:
                variance = max(total_sq / count - mean * mean, 0.0)
                stds[i] = np.sqrt(variance)
            else:
                stds[i] = 0.0
        count += 1
        total += float(amounts[i])
        total_sq += float(amounts[i] * amounts[i])
    return means, stds


def amount_zscore(amounts: np.ndarray, prior_mean: np.ndarray, prior_std: np.ndarray) -> np.ndarray:
    """Standardize the current amount against prior history. Missing history is 0."""
    z = np.zeros(len(amounts), dtype=np.float64)
    valid = np.isfinite(prior_mean) & np.isfinite(prior_std) & (prior_std > 1e-8)
    z[valid] = (amounts[valid] - prior_mean[valid]) / prior_std[valid]
    return z
