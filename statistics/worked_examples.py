"""Fraud-rate comparison used by the statistics interview.

``two_proportion_ztest`` reports rate_a minus rate_b. A move from 0.15% to
0.35% is a positive business change and a negative value of ``difference``
when period A is the earlier rate. Read the sign before you brief it.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from evaluation.inference import two_proportion_ztest


def _wald(successes: int, n: int) -> tuple[float, float]:
    p = successes / n
    se = math.sqrt(p * (1.0 - p) / n)
    z = 1.959963984540054
    return p - z * se, p + z * se


def fraud_rate_change(successes_a: int, n_a: int, successes_b: int, n_b: int) -> dict:
    """Compare two independent fraud rates and attach Wald intervals."""
    result = two_proportion_ztest(successes_a, n_a, successes_b, n_b)
    result["interval_a"] = _wald(successes_a, n_a)
    result["interval_b"] = _wald(successes_b, n_b)
    return result
