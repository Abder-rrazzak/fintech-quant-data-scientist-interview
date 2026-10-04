"""Returns, autocorrelation, a transparent AR(1), and lag matrices.

Random row shuffles are intentionally absent. Forecasting code consumes
chronological arrays.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def simple_returns(prices: np.ndarray) -> np.ndarray:
    prices = np.asarray(prices, dtype=float)
    return np.diff(prices) / prices[:-1]


def log_returns(prices: np.ndarray) -> np.ndarray:
    prices = np.asarray(prices, dtype=float)
    if np.any(prices <= 0):
        raise ValueError("Log returns require strictly positive prices.")
    return np.diff(np.log(prices))


def rolling_mean(values: np.ndarray, window: int) -> np.ndarray:
    series = pd.Series(np.asarray(values, dtype=float))
    return series.rolling(window, min_periods=window).mean().to_numpy()


def rolling_volatility(returns: np.ndarray, window: int) -> np.ndarray:
    series = pd.Series(np.asarray(returns, dtype=float))
    return series.rolling(window, min_periods=window).std(ddof=1).to_numpy()


def acf(values: np.ndarray, nlags: int) -> np.ndarray:
    """Sample autocorrelation using the n-divisor convention."""
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    x = x - x.mean()
    denominator = float(np.dot(x, x))
    out = np.empty(nlags + 1, dtype=float)
    out[0] = 1.0
    if denominator == 0:
        out[1:] = 0.0
        return out
    for lag in range(1, nlags + 1):
        out[lag] = float(np.dot(x[:-lag], x[lag:]) / denominator)
    return out


def pacf_durbin_levinson(values: np.ndarray, nlags: int) -> np.ndarray:
    """Partial autocorrelation via Durbin-Levinson. Index 0 is 1."""
    rho = acf(values, nlags)
    pacf = np.zeros(nlags + 1, dtype=float)
    pacf[0] = 1.0
    if nlags == 0:
        return pacf
    phi = np.zeros((nlags + 1, nlags + 1), dtype=float)
    phi[1, 1] = rho[1]
    pacf[1] = phi[1, 1]
    for k in range(2, nlags + 1):
        prev = phi[k - 1, 1:k]
        acc = float(np.dot(prev, rho[1:k][::-1]))
        denom = 1.0 - float(np.dot(prev, rho[1:k]))
        phi[k, k] = 0.0 if abs(denom) < 1e-12 else (rho[k] - acc) / denom
        for j in range(1, k):
            phi[k, j] = phi[k - 1, j] - phi[k, k] * phi[k - 1, k - j]
        pacf[k] = phi[k, k]
    return pacf


def fit_ar1(values: np.ndarray) -> tuple[float, float]:
    """OLS AR(1) with intercept. Returns ``(intercept, phi)``."""
    y = np.asarray(values, dtype=float)
    y = y[np.isfinite(y)]
    if len(y) < 3:
        raise ValueError("AR(1) needs at least 3 observations.")
    target = y[1:]
    design = np.column_stack([np.ones(len(target)), y[:-1]])
    beta, *_ = np.linalg.lstsq(design, target, rcond=None)
    return float(beta[0]), float(beta[1])


def lag_matrix(values: np.ndarray, lags: int) -> tuple[np.ndarray, np.ndarray]:
    """Supervised matrix where row t uses only values at t-1 ... t-lags."""
    y = np.asarray(values, dtype=float)
    rows = []
    targets = []
    for t in range(lags, len(y)):
        rows.append(y[t - lags : t][::-1])
        targets.append(y[t])
    return np.asarray(rows, dtype=float), np.asarray(targets, dtype=float)
