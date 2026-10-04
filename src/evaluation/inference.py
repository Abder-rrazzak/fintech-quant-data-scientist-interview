"""Small statistical routines used in interview answers and tests.

Implementations are teaching versions of standard formulas, not a replacement
for a reviewed statistical library in a regulated model validation document.
"""

from __future__ import annotations

import math

import numpy as np


def sigmoid(logit: np.ndarray | float) -> np.ndarray | float:
    value = np.asarray(logit, dtype=float)
    out = 1.0 / (1.0 + np.exp(-np.clip(value, -30, 30)))
    if np.isscalar(logit):
        return float(out)
    return out


def two_proportion_ztest(
    success_a: int, n_a: int, success_b: int, n_b: int
) -> dict[str, float]:
    """Two-sided z-test for a difference in independent proportions.

    Use this for a fraud-rate or approval-rate change when each trial is an
    independent event and the sample is large enough for the normal approximation.
    """
    if min(n_a, n_b) <= 0:
        raise ValueError("Sample sizes must be positive.")
    p1 = success_a / n_a
    p2 = success_b / n_b
    pooled = (success_a + success_b) / (n_a + n_b)
    se = math.sqrt(pooled * (1.0 - pooled) * (1.0 / n_a + 1.0 / n_b))
    z = 0.0 if se == 0 else (p1 - p2) / se
    p_value = math.erfc(abs(z) / math.sqrt(2.0))
    return {
        "z": float(z),
        "p_value": float(p_value),
        "rate_a": float(p1),
        "rate_b": float(p2),
        "difference": float(p1 - p2),
    }


def normal_confidence_interval(values: np.ndarray, level: float = 0.95) -> tuple[float, float]:
    """Mean confidence interval using the normal critical value and sample sd."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    if n < 2:
        raise ValueError("Need at least two observations.")
    mean = float(values.mean())
    sd = float(values.std(ddof=1))
    # 1.95996398454 is the 97.5% standard normal quantile.
    z = 1.959963984540054 if abs(level - 0.95) < 1e-9 else _approx_z(level)
    half = z * sd / math.sqrt(n)
    return mean - half, mean + half


def _approx_z(level: float) -> float:
    if not 0 < level < 1:
        raise ValueError("Confidence level must be between 0 and 1.")
    # Beasley-Springer-Moro style rational approximation is unnecessary here.
    # The lab defaults to 95%. Other levels use a short Newton solve on erfc.
    target = (1.0 + level) / 2.0

    def cdf(z: float) -> float:
        return 0.5 * math.erfc(-z / math.sqrt(2.0))

    z = 0.0
    for _ in range(20):
        # derivative of cdf is the normal density
        density = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        z -= (cdf(z) - target) / density
    return z


def bootstrap_mean_interval(
    values: np.ndarray, n_resamples: int = 1000, level: float = 0.95, seed: int = 42
) -> tuple[float, float]:
    """Percentile bootstrap interval for the mean."""
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    draws = rng.choice(values, size=(n_resamples, len(values)), replace=True)
    means = draws.mean(axis=1)
    alpha = (1.0 - level) / 2.0
    low, high = np.quantile(means, [alpha, 1.0 - alpha])
    return float(low), float(high)
