"""Customer value: RFM, a margin identity, and a horizon revenue model.

Simple CLV multiplies observed value by a lifespan assumption. Predictive CLV
replaces that assumption with a model of future revenue. Neither is a
contractual BG/NBD model; both are explicit enough to defend in an interview.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error


def rfm_table(transactions: pd.DataFrame, snapshot: pd.Timestamp | None = None) -> pd.DataFrame:
    frame = transactions.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    snapshot_ts = pd.Timestamp(snapshot or frame["timestamp"].max())
    grouped = frame.groupby("customer_id", sort=True)
    table = pd.DataFrame(
        {
            "recency_days": (snapshot_ts - grouped["timestamp"].max()).dt.days,
            "frequency": grouped["transaction_id"].nunique(),
            "monetary": grouped["amount"].sum(),
        }
    ).reset_index()
    table["snapshot"] = snapshot_ts
    return table


def simple_clv(
    avg_order_value: float,
    purchases_per_period: float,
    margin: float,
    lifespan_periods: float,
) -> float:
    """Historical CLV = AOV x purchase rate x margin x assumed remaining life."""
    if margin < 0 or lifespan_periods < 0 or purchases_per_period < 0:
        raise ValueError("Margin, lifespan, and purchase rate must be non-negative.")
    return float(avg_order_value * purchases_per_period * margin * lifespan_periods)


def horizon_revenue_frame(
    transactions: pd.DataFrame, cutoff: pd.Timestamp, horizon_days: int = 90
) -> pd.DataFrame:
    """One row per customer with pre-cutoff RFM and post-cutoff revenue.

    The label uses only the horizon after ``cutoff``. Features use only history
    before ``cutoff``.
    """
    frame = transactions.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    cutoff_ts = pd.Timestamp(cutoff)
    horizon_end = cutoff_ts + pd.Timedelta(days=horizon_days)
    past = frame.loc[frame["timestamp"] < cutoff_ts]
    future = frame.loc[(frame["timestamp"] >= cutoff_ts) & (frame["timestamp"] < horizon_end)]
    if past.empty:
        return pd.DataFrame()
    features = rfm_table(past, snapshot=cutoff_ts).drop(columns=["snapshot"])
    revenue = future.groupby("customer_id")["amount"].sum().rename("future_revenue")
    out = features.merge(revenue, on="customer_id", how="left")
    out["future_revenue"] = out["future_revenue"].fillna(0.0)
    out["cutoff"] = cutoff_ts
    out["horizon_days"] = horizon_days
    return out


def fit_predictive_clv(frame: pd.DataFrame, margin: float = 0.25) -> dict:
    """Predict horizon revenue from RFM and convert it to a margin-adjusted CLV."""
    if len(frame) < 20:
        raise ValueError("Need at least 20 customers to fit a predictive CLV demo.")
    features = ["recency_days", "frequency", "monetary"]
    ordered = frame.sort_values("customer_id")
    split = max(1, int(len(ordered) * 0.75))
    train = ordered.iloc[:split]
    test = ordered.iloc[split:]
    model = HistGradientBoostingRegressor(max_depth=3, max_iter=80, random_state=42)
    model.fit(train[features], train["future_revenue"])
    pred = np.clip(model.predict(test[features]), 0, None)
    mae = float(mean_absolute_error(test["future_revenue"], pred)) if len(test) else float("nan")
    return {
        "model": model,
        "features": features,
        "margin": margin,
        "test_mae": mae,
        "test_predicted_clv": pred * margin,
    }
