"""Transaction features that are knowable when the transaction is authorized.

``balance_after``, fraud labels, and investigator detection times are not features.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from config.settings import SETTINGS
from features.windows import amount_zscore, prior_mean_and_std, window_count_and_sum

HOUR_NS = 3_600_000_000_000
DAY_NS = 24 * HOUR_NS


def engineer_fraud_features(transactions: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Return a frame sorted by customer and time with authorization-time features."""
    required = {"customer_id", "timestamp", "amount", "country", "device_id", "merchant_category"}
    missing = required.difference(transactions.columns)
    if missing:
        raise ValueError(f"Transactions are missing columns: {sorted(missing)}")
    frame = transactions.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    frame = frame.sort_values(["customer_id", "timestamp"], kind="mergesort").reset_index(drop=True)

    home = customers.set_index("customer_id")["country"]
    frame["home_country"] = frame["customer_id"].map(home)
    frame["geo_mismatch"] = (
        frame["home_country"].notna() & frame["country"].notna() & (frame["country"] != frame["home_country"])
    ).astype(int)
    frame["hour"] = frame["timestamp"].dt.hour.astype(int)
    frame["night"] = frame["hour"].between(0, 5).astype(int)
    frame["high_risk_mcc"] = frame["merchant_category"].isin(SETTINGS.high_risk_categories).astype(int)
    frame["log_amount"] = np.log1p(frame["amount"].clip(lower=0))
    frame["new_device"] = (
        frame.groupby(["customer_id", "device_id"], sort=False).cumcount().to_numpy() == 0
    ).astype(int)

    entity = frame["customer_id"].to_numpy()
    timestamps = frame["timestamp"].to_numpy(dtype="datetime64[ns]").view(np.int64)
    amounts = frame["amount"].to_numpy(dtype=float)
    count_1h, _ = window_count_and_sum(entity, timestamps, amounts, HOUR_NS)
    count_24h, sum_24h = window_count_and_sum(entity, timestamps, amounts, DAY_NS)
    prior_mean, prior_std = prior_mean_and_std(entity, amounts)
    frame["txn_count_1h"] = count_1h
    frame["txn_count_24h"] = count_24h
    frame["amount_sum_24h"] = sum_24h
    frame["prior_amount_mean"] = prior_mean
    frame["prior_amount_std"] = prior_std
    frame["amount_zscore"] = amount_zscore(amounts, prior_mean, prior_std)
    return frame


def fraud_rule_score(frame: pd.DataFrame) -> np.ndarray:
    """Transparent baseline score in ``[0, 1]`` from velocity, amount, and geography."""
    z = np.clip(frame["amount_zscore"].fillna(0).to_numpy(dtype=float), 0, 5) / 5.0
    velocity = np.clip(frame["txn_count_1h"].to_numpy(dtype=float), 0, 10) / 10.0
    geo = frame["geo_mismatch"].to_numpy(dtype=float)
    device = frame["new_device"].to_numpy(dtype=float)
    return 0.45 * z + 0.25 * velocity + 0.15 * geo + 0.15 * device
