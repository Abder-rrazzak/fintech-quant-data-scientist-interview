"""Paths, costs, and shared feature contracts.

Portfolio laboratory settings only. Nothing here is a production secret.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    """Runtime locations and decision costs for the synthetic lab."""

    repo_root: Path = field(default_factory=_repo_root)
    seed: int = 42
    false_negative_cost: float = 500.0
    false_positive_cost: float = 5.0
    high_risk_categories: tuple[str, ...] = (
        "gambling",
        "crypto",
        "wire",
        "luxury",
    )
    fraud_numeric: tuple[str, ...] = (
        "amount",
        "log_amount",
        "hour",
        "night",
        "geo_mismatch",
        "new_device",
        "high_risk_mcc",
        "txn_count_1h",
        "txn_count_24h",
        "amount_sum_24h",
        "amount_zscore",
        "account_age_days",
        "customer_age",
    )
    fraud_categorical: tuple[str, ...] = (
        "merchant_category",
        "payment_method",
        "customer_segment",
    )
    credit_numeric: tuple[str, ...] = (
        "income",
        "credit_score",
        "utilization",
        "dti",
        "account_age_days",
        "prior_delinquency_count",
        "principal",
        "interest_rate",
        "txn_count_90d",
        "avg_amount_90d",
    )
    credit_categorical: tuple[str, ...] = ("employment_status", "customer_segment")
    fraud_target: str = "is_fraud"
    credit_target: str = "default_12m"
    # Columns that are outcomes or post-decision facts. Never use them as features.
    leakage_columns: tuple[str, ...] = (
        "is_fraud",
        "fraud_type",
        "defaulted",
        "default_12m",
        "balance_after",
        "label",
        "target",
        "detected_at",
        "expected_loss",
    )

    @property
    def data_raw(self) -> Path:
        return self.repo_root / "data" / "raw"

    @property
    def data_processed(self) -> Path:
        return self.repo_root / "data" / "processed"

    @property
    def data_sample(self) -> Path:
        return self.repo_root / "data" / "sample"

    @property
    def artifacts(self) -> Path:
        return self.repo_root / "artifacts"

    @property
    def question_bank(self) -> Path:
        return self.repo_root / "mock-interviews" / "question_bank.json"


SETTINGS = Settings()
