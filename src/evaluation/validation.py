"""Time-aware splits and leakage checks.

Random K-fold on transactions or on a price path leaks the future into the past.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from config.settings import SETTINGS


class LeakageError(ValueError):
    """Raised when a feature set or a time index violates a training contract."""


def find_leaky_columns(columns: list[str] | tuple[str, ...]) -> list[str]:
    """Flag outcome and post-decision columns by exact name."""
    banned = set(SETTINGS.leakage_columns)
    return [column for column in columns if column in banned]


def assert_no_leaky_columns(columns: list[str] | tuple[str, ...]) -> None:
    found = find_leaky_columns(columns)
    if found:
        raise LeakageError(f"Leakage columns in feature list: {found}")


def assert_point_in_time(feature_times: np.ndarray, decision_times: np.ndarray) -> None:
    """Every feature timestamp must be known at or before the decision."""
    feature_times = pd.to_datetime(feature_times).to_numpy(dtype="datetime64[ns]")
    decision_times = pd.to_datetime(decision_times).to_numpy(dtype="datetime64[ns]")
    if len(feature_times) != len(decision_times):
        raise LeakageError("Feature times and decision times have different lengths.")
    if np.any(feature_times > decision_times):
        raise LeakageError("At least one feature timestamp is after its decision time.")


def calendar_split(
    frame: pd.DataFrame,
    time_col: str,
    train_end: str,
    valid_end: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    times = pd.to_datetime(frame[time_col])
    train = frame.loc[times <= pd.Timestamp(train_end)].copy()
    valid = frame.loc[(times > pd.Timestamp(train_end)) & (times <= pd.Timestamp(valid_end))].copy()
    test = frame.loc[times > pd.Timestamp(valid_end)].copy()
    return train, valid, test


def quantile_time_split(
    frame: pd.DataFrame,
    time_col: str,
    train_q: float = 0.70,
    valid_q: float = 0.85,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Time-ordered 70/15/15 split used only when a calendar bucket is too small."""
    ordered = frame.sort_values(time_col, kind="mergesort")
    n = len(ordered)
    i = max(1, int(n * train_q))
    j = max(i + 1, int(n * valid_q))
    j = min(j, n - 1)
    return ordered.iloc[:i].copy(), ordered.iloc[i:j].copy(), ordered.iloc[j:].copy()


def split_for_training(
    frame: pd.DataFrame,
    time_col: str,
    train_end: str,
    valid_end: str,
    target: str,
    min_rows: int = 40,
    min_positives: int = 3,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str]:
    """Prefer calendar boundaries. Fall back to a time-ordered quantile split."""
    train, valid, test = calendar_split(frame, time_col, train_end, valid_end)
    buckets = (train, valid, test)

    def _thin(part: pd.DataFrame) -> bool:
        if len(part) < min_rows:
            return True
        return int(part[target].sum()) < min_positives or int((part[target] == 0).sum()) < min_positives

    if any(_thin(part) for part in buckets):
        train, valid, test = quantile_time_split(frame, time_col)
        return train, valid, test, "time_quantile_fallback"
    return train, valid, test, "calendar"
