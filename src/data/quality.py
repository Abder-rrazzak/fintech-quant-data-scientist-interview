"""Schema and row-level checks for synthetic transactions.

Raw extracts are expected to fail. The training table is expected to pass.
Pandera is used when it imports cleanly; the manual checks remain the contract.
"""

from __future__ import annotations

import pandas as pd

from config.settings import SETTINGS

TRANSACTION_COLUMNS = [
    "transaction_id",
    "customer_id",
    "account_id",
    "merchant_id",
    "timestamp",
    "amount",
    "currency",
    "country",
    "merchant_category",
    "payment_method",
    "device_id",
    "ip_address",
    "account_age_days",
    "customer_age",
    "customer_segment",
    "balance_before",
    "balance_after",
    "transaction_type",
    "is_fraud",
]

CURRENCIES = {"USD", "EUR", "GBP"}


def quality_report(transactions: pd.DataFrame) -> dict:
    """Summarize the problems a raw financial extract usually has."""
    frame = transactions.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
    negative_purchases = int(
        ((frame["transaction_type"] == "purchase") & (frame["amount"] < 0)).sum()
    )
    ages = frame["customer_age"]
    invalid_age = int((~ages.between(18, 100) | ages.isna()).sum())
    return {
        "rows": int(len(frame)),
        "duplicate_transaction_ids": int(frame["transaction_id"].duplicated().sum()),
        "missing_by_column": {col: int(frame[col].isna().sum()) for col in frame.columns},
        "negative_purchase_amounts": negative_purchases,
        "invalid_customer_age": invalid_age,
        "null_timestamps": int(frame["timestamp"].isna().sum()),
        "fraud_rate": float(frame["is_fraud"].mean()) if len(frame) else 0.0,
    }


def validate_transactions(transactions: pd.DataFrame, strict: bool = False) -> list[str]:
    """Return human-readable issues. ``strict`` is the training-table contract."""
    issues: list[str] = []
    missing_cols = [col for col in TRANSACTION_COLUMNS if col not in transactions.columns]
    if missing_cols:
        issues.append(f"Missing columns: {missing_cols}")
        return issues
    if transactions["transaction_id"].duplicated().any():
        issues.append("Duplicate transaction_id values.")
    if transactions["timestamp"].isna().any():
        issues.append("Null timestamps.")
    if ((transactions["transaction_type"] == "purchase") & (transactions["amount"] < 0)).any():
        issues.append("Negative amounts on purchases.")
    if (~transactions["customer_age"].between(18, 100)).any():
        issues.append("customer_age outside 18-100.")
    if (~transactions["currency"].isin(CURRENCIES)).any():
        issues.append("Unexpected currency codes.")
    if (~transactions["is_fraud"].isin([0, 1])).any():
        issues.append("is_fraud is not 0/1.")
    if strict and issues:
        return issues
    return issues


def clean_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicates and rows that violate the training contract.

    The first copy of a duplicated transaction id is kept. Negative purchases
    are removed rather than silently flipped, because the sign may be a defect
    or a mis-typed refund.
    """
    frame = transactions.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
    frame = frame.dropna(subset=["timestamp", "customer_id", "amount", "transaction_id"])
    frame = frame.sort_values("timestamp", kind="mergesort")
    frame = frame.drop_duplicates("transaction_id", keep="first")
    negative_purchase = (frame["transaction_type"] == "purchase") & (frame["amount"] < 0)
    frame = frame.loc[~negative_purchase]
    frame = frame.loc[frame["customer_age"].between(18, 100)]
    frame["merchant_category"] = frame["merchant_category"].fillna("unknown")
    frame["device_id"] = frame["device_id"].fillna("unknown_device")
    frame = frame.loc[frame["currency"].isin(CURRENCIES)]
    frame["is_fraud"] = frame["is_fraud"].astype(int)
    return frame.reset_index(drop=True)


def pandera_transaction_schema():
    """Optional Pandera schema for the cleaned training table."""
    import pandera.pandas as pa

    return pa.DataFrameSchema(
        {
            "transaction_id": pa.Column(int, unique=True),
            "amount": pa.Column(float),
            "is_fraud": pa.Column(int, checks=pa.Check.isin([0, 1])),
            "customer_age": pa.Column(int, checks=pa.Check.in_range(18, 100)),
            "currency": pa.Column(str, checks=pa.Check.isin(list(CURRENCIES))),
        },
        coerce=True,
    )


def training_columns_are_safe(columns: list[str]) -> bool:
    return not any(column in SETTINGS.leakage_columns for column in columns)
