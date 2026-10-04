"""Point-in-time credit features.

Transaction statistics for a loan use only activity strictly before origination.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class TransactionHistory:
    """Per-customer timestamp and amount arrays for as-of lookups."""

    def __init__(self, transactions: pd.DataFrame) -> None:
        frame = transactions.copy()
        frame["timestamp"] = pd.to_datetime(frame["timestamp"])
        frame = frame.sort_values(["customer_id", "timestamp"], kind="mergesort")
        self._groups: dict[int, tuple[np.ndarray, np.ndarray]] = {}
        for customer_id, group in frame.groupby("customer_id", sort=False):
            self._groups[int(customer_id)] = (
                group["timestamp"].to_numpy(dtype="datetime64[ns]"),
                group["amount"].to_numpy(dtype=float),
            )

    def window_stats(self, customer_id: int, cutoff: pd.Timestamp, window_days: int = 90) -> tuple[int, float]:
        arrays = self._groups.get(int(customer_id))
        if arrays is None:
            return 0, 0.0
        timestamps, amounts = arrays
        cutoff64 = np.datetime64(pd.Timestamp(cutoff).to_datetime64(), "ns")
        start = cutoff64 - np.timedelta64(int(window_days), "D")
        hi = int(np.searchsorted(timestamps, cutoff64, side="left"))
        lo = int(np.searchsorted(timestamps, start, side="left"))
        slab = amounts[lo:hi]
        if slab.size == 0:
            return 0, 0.0
        return int(slab.size), float(slab.mean())


def attach_credit_transaction_features(
    loans: pd.DataFrame, transactions: pd.DataFrame, window_days: int = 90
) -> pd.DataFrame:
    """Add ``txn_count_90d`` and ``avg_amount_90d`` known at origination."""
    history = TransactionHistory(transactions)
    counts: list[int] = []
    averages: list[float] = []
    for row in loans.itertuples(index=False):
        count, average = history.window_stats(int(row.customer_id), row.origination_date, window_days)
        counts.append(count)
        averages.append(average)
    out = loans.copy()
    out["txn_count_90d"] = counts
    out["avg_amount_90d"] = averages
    return out
