"""Local scoring API for the laboratory.

The service scores feature vectors that were already computed with the same
definitions as training. It does not claim to be an authorized production
decision system.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from config.settings import SETTINGS
from fraud.decisions import decide
from pipelines.training import score_frame


class FraudFeatures(BaseModel):
    amount: float
    log_amount: float
    hour: int
    night: int
    geo_mismatch: int
    new_device: int
    high_risk_mcc: int
    txn_count_1h: float
    txn_count_24h: float
    amount_sum_24h: float
    amount_zscore: float
    account_age_days: float
    customer_age: float
    merchant_category: str = "grocery"
    payment_method: str = "card_not_present"
    customer_segment: str = "retail"


class CreditFeatures(BaseModel):
    income: float
    credit_score: float = Field(ge=300, le=850)
    utilization: float
    dti: float
    account_age_days: float
    prior_delinquency_count: float
    principal: float
    interest_rate: float
    txn_count_90d: float
    avg_amount_90d: float
    employment_status: str = "employed"
    customer_segment: str = "retail"


def create_app(artifact_dir: Path | None = None) -> FastAPI:
    root = Path(artifact_dir) if artifact_dir is not None else SETTINGS.artifacts
    application = FastAPI(title="Financial Intelligence Lab", version="1.0.0")
    cache: dict[str, dict | None] = {"fraud": None, "credit": None}

    def load(name: str) -> dict:
        if cache[name] is None:
            path = root / name / "model.joblib"
            if not path.exists():
                raise HTTPException(
                    status_code=503,
                    detail=f"No {name} artifact at {path}. Run scripts/train.py.",
                )
            cache[name] = joblib.load(path)
        artifact = cache[name]
        assert artifact is not None
        return artifact

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": "synthetic-lab"}

    @application.post("/score/fraud")
    def score_fraud(body: FraudFeatures) -> dict:
        artifact = load("fraud")
        frame = pd.DataFrame([body.model_dump()])
        probability = float(score_frame(artifact, frame)[0])
        decision = str(
            decide([probability], artifact["review_threshold"], artifact["block_threshold"])[0]
        )
        return {
            "probability": probability,
            "decision": decision,
            "review_threshold": artifact["review_threshold"],
            "block_threshold": artifact["block_threshold"],
            "disclaimer": "Synthetic laboratory score. Not a production fraud decision.",
        }

    @application.post("/score/credit")
    def score_credit(body: CreditFeatures) -> dict:
        artifact = load("credit")
        frame = pd.DataFrame([body.model_dump()])
        probability = float(score_frame(artifact, frame)[0])
        return {
            "probability_of_default": probability,
            "disclaimer": "Synthetic laboratory PD. Not a credit decision or a regulatory capital input.",
        }

    return application


app = create_app()
