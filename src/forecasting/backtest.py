"""Walk-forward and rolling evaluation.

Backtesting is not random cross-validation. The test window always sits
strictly after the training window, and features inside that test window
cannot use later rows.
"""

from __future__ import annotations

import numpy as np


def expanding_window_indices(
    n: int, min_train: int, test_size: int, step: int | None = None
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Train on ``[0, start)`` and test on ``[start, start + test_size)``."""
    if min_train < 1 or test_size < 1:
        raise ValueError("min_train and test_size must be positive.")
    step = test_size if step is None else step
    if step < 1:
        raise ValueError("step must be positive.")
    splits: list[tuple[np.ndarray, np.ndarray]] = []
    start = min_train
    while start + test_size <= n:
        train_idx = np.arange(0, start)
        test_idx = np.arange(start, start + test_size)
        splits.append((train_idx, test_idx))
        start += step
    return splits


def rolling_window_indices(
    n: int, train_size: int, test_size: int, step: int | None = None
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Fixed-length train window immediately before each test window."""
    if train_size < 1 or test_size < 1:
        raise ValueError("train_size and test_size must be positive.")
    step = test_size if step is None else step
    splits: list[tuple[np.ndarray, np.ndarray]] = []
    start = train_size
    while start + test_size <= n:
        train_idx = np.arange(start - train_size, start)
        test_idx = np.arange(start, start + test_size)
        splits.append((train_idx, test_idx))
        start += step
    return splits


def assert_causal_splits(splits: list[tuple[np.ndarray, np.ndarray]]) -> None:
    for train_idx, test_idx in splits:
        if len(train_idx) == 0 or len(test_idx) == 0:
            raise AssertionError("Empty split.")
        if train_idx.max() >= test_idx.min():
            raise AssertionError("Training index overlaps or follows the test index.")


def apply_transaction_cost(gross_return: float, turnover: float, cost_bps: float) -> float:
    """Subtract a proportional cost. ``cost_bps`` is basis points of turnover."""
    return float(gross_return - turnover * cost_bps / 10_000.0)


def slippage_adjusted_price(price: float, side: str, slippage_bps: float) -> float:
    """Buy higher and sell lower by a slippage assumption. This is not a fill model."""
    bump = slippage_bps / 10_000.0
    if side == "buy":
        return float(price * (1.0 + bump))
    if side == "sell":
        return float(price * (1.0 - bump))
    raise ValueError("side must be 'buy' or 'sell'.")


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    error = y_pred - y_true
    mae = float(np.mean(np.abs(error)))
    rmse = float(np.sqrt(np.mean(error**2)))
    denom = np.abs(y_true)
    mape_mask = denom > 1e-8
    mape = float(np.mean(np.abs(error[mape_mask] / y_true[mape_mask]))) if mape_mask.any() else float("nan")
    return {"mae": mae, "rmse": rmse, "mape": mape}
