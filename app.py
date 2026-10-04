"""Financial intelligence laboratory dashboard.

Scores come from a saved artifact when one exists. Otherwise the page uses the
transparent rule baseline so the decision loop is still visible. This is a
synthetic portfolio demo, not a production decision system.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from config.settings import SETTINGS  # noqa: E402
from features.transactions import fraud_rule_score  # noqa: E402
from fraud.decisions import decide  # noqa: E402


st.set_page_config(page_title="Financial intelligence lab", layout="wide")
st.title("Financial intelligence lab")
st.caption(
    "Synthetic portfolio demonstration. It does not describe a live fraud book, "
    "a credit book, or employment at a financial institution."
)


def _rule_row(amount_z: float, velocity: float, geo: bool, new_device: bool) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "amount_zscore": amount_z,
                "txn_count_1h": velocity,
                "geo_mismatch": int(geo),
                "new_device": int(new_device),
            }
        ]
    )


left, right = st.columns(2)
with left:
    st.subheader("Transaction")
    amount_z = st.slider("Amount z-score versus this customer", 0.0, 5.0, 1.0, 0.1)
    velocity = st.slider("Transactions in the last hour, including this one", 0.0, 10.0, 1.0, 1.0)
    geo = st.checkbox("Country differs from the customer home country")
    new_device = st.checkbox("Device has not been seen for this customer")
    review = st.slider("Review threshold", 0.05, 0.95, 0.35, 0.05)
    block = st.slider("Block threshold", float(review), 0.99, max(0.70, float(review)), 0.05)

row = _rule_row(amount_z, velocity, geo, new_device)
rule = float(fraud_rule_score(row)[0])
rule_decision = str(decide([rule], review, block)[0])

@st.cache_resource
def _load_fraud_artifact():
    path = SETTINGS.artifacts / "fraud" / "model.joblib"
    if not path.exists():
        return None
    import joblib

    return joblib.load(path)


artifact = _load_fraud_artifact()
model_score = None
model_decision = None
if artifact is not None:
    from pipelines.training import score_frame

    featured = pd.DataFrame(
        [
            {
                "amount": 80.0,
                "log_amount": 4.4,
                "hour": 2 if geo else 14,
                "night": int(geo),
                "geo_mismatch": int(geo),
                "new_device": int(new_device),
                "high_risk_mcc": int(amount_z >= 3),
                "txn_count_1h": velocity,
                "txn_count_24h": max(velocity, 1.0),
                "amount_sum_24h": 80.0 * max(velocity, 1.0),
                "amount_zscore": amount_z,
                "account_age_days": 40.0 if new_device else 400.0,
                "customer_age": 35.0,
                "merchant_category": "wire" if geo else "grocery",
                "payment_method": "card_not_present",
                "customer_segment": "retail",
            }
        ]
    )
    model_score = float(score_frame(artifact, featured)[0])
    model_decision = str(
        decide([model_score], float(artifact["review_threshold"]), float(artifact["block_threshold"]))[0]
    )

with right:
    st.subheader("Rule decision")
    st.metric("Rule score", f"{rule:.3f}")
    st.metric("Rule decision", rule_decision)
    st.caption("The sliders set this baseline. It is the transparent score a model has to beat.")
    if rule_decision == "block":
        st.error("Block. The rule score is at or above the block threshold.")
    elif rule_decision == "review":
        st.warning("Review. A person still has to look at the case.")
    else:
        st.success("Approve. The rule score is below the review threshold.")
    if model_score is not None:
        st.subheader("Saved model")
        st.metric("Model score", f"{model_score:.3f}")
        st.metric("Model decision", model_decision)
        st.caption(
            f"{artifact.get('model_name', 'model')} using the validation thresholds "
            f"({float(artifact['review_threshold']):.3f} review / {float(artifact['block_threshold']):.3f} block). "
            "This one hand-built row is not a portfolio result."
        )
    st.write(
        f"False negative cost ${SETTINGS.false_negative_cost:.0f}. "
        f"False positive cost ${SETTINGS.false_positive_cost:.0f}."
    )

summary = SETTINGS.artifacts / "evaluation_summary.md"
if summary.exists():
    st.subheader("Latest laboratory evaluation")
    st.markdown(summary.read_text(encoding="utf-8"))
else:
    st.info("Train a model with `python scripts/train.py` to replace the rule score with a saved artifact.")
