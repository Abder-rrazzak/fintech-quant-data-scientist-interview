"""A local stand-in for the batch path S3 -> features -> score -> decision log.

No AWS account is required. The same stages are files in this repository:
raw Parquet, a feature frame, a joblib artifact, and a decision log.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from features.transactions import engineer_fraud_features
from fraud.decisions import decide
from pipelines.training import score_frame


def score_batch(transactions: pd.DataFrame, customers: pd.DataFrame, artifact: dict, output: Path) -> pd.DataFrame:
    features = engineer_fraud_features(transactions, customers)
    scores = score_frame(artifact, features)
    decisions = decide(scores, artifact["review_threshold"], artifact["block_threshold"])
    log = pd.DataFrame(
        {
            "transaction_id": features["transaction_id"].to_numpy(),
            "score": scores,
            "decision": decisions,
            "model_name": artifact.get("model_name", "unknown"),
        }
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    log.to_csv(output, index=False)
    return log
