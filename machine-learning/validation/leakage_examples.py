"""Small frames that show leakage a split metric will not catch by itself."""

from __future__ import annotations

import pandas as pd

from evaluation.validation import find_leaky_columns


def future_mean_attached_to_the_past(transactions: pd.DataFrame) -> pd.DataFrame:
    """A customer-month mean computed on the whole month, copied onto every row.

    A transaction on 3 March then carries spend that happens on 28 March.
    """
    frame = transactions.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    frame["month"] = frame["timestamp"].dt.to_period("M").astype(str)
    month_mean = frame.groupby(["customer_id", "month"])["amount"].transform("mean")
    frame["month_mean_including_future"] = month_mean
    return frame


def columns_that_must_not_be_features() -> list[str]:
    """Names the training contract rejects even if a notebook selects them."""
    return find_leaky_columns(["amount", "is_fraud", "balance_after", "utilization"])
