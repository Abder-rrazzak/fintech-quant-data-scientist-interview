"""Train fraud and credit classifiers and write a business-facing summary.

The selected threshold is chosen on the validation window only. The test window
is scored once, after that choice.
"""

from __future__ import annotations

import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config.settings import SETTINGS
from data.generate import load_raw
from data.quality import clean_transactions
from evaluation.calibration import apply_platt, fit_platt
from evaluation.metrics import classification_bundle, safe_pr_auc, safe_roc_auc
from evaluation.thresholds import plot_cost_curve, select_threshold, threshold_cost_curve
from evaluation.validation import assert_no_leaky_columns, split_for_training
from features.credit_features import attach_credit_transaction_features
from features.transactions import engineer_fraud_features, fraud_rule_score
from fraud.decisions import decide
from monitoring.drift import psi_table
from monitoring.report import render_monitoring_report
from utils.io import write_json

logger = logging.getLogger(__name__)


def run_training(raw_dir: Path, artifact_dir: Path) -> dict:
    """Train both laboratory models from a raw synthetic extract."""
    tables = load_raw(raw_dir)
    transactions = clean_transactions(tables["transactions"])
    fraud_frame = engineer_fraud_features(transactions, tables["customers"])
    credit_frame = attach_credit_transaction_features(tables["loans"], transactions)

    fraud_metrics, fraud_artifact = _train_one(
        fraud_frame,
        time_col="timestamp",
        train_end="2024-12-31",
        valid_end="2025-06-01",
        target=SETTINGS.fraud_target,
        numeric=list(SETTINGS.fraud_numeric),
        categorical=list(SETTINGS.fraud_categorical),
        primary="pr_auc",
        baseline_scores=fraud_rule_score(fraud_frame),
    )
    credit_baseline = ((850.0 - credit_frame["credit_score"].to_numpy(dtype=float)) / 550.0).clip(0, 1)
    credit_metrics, credit_artifact = _train_one(
        credit_frame,
        time_col="origination_date",
        train_end="2023-12-31",
        valid_end="2024-06-30",
        target=SETTINGS.credit_target,
        numeric=list(SETTINGS.credit_numeric),
        categorical=list(SETTINGS.credit_categorical),
        primary="roc_auc",
        baseline_scores=credit_baseline,
    )

    fraud_dir = artifact_dir / "fraud"
    credit_dir = artifact_dir / "credit"
    fraud_dir.mkdir(parents=True, exist_ok=True)
    credit_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(fraud_artifact, fraud_dir / "model.joblib")
    joblib.dump(credit_artifact, credit_dir / "model.joblib")
    write_json(fraud_dir / "metrics.json", fraud_metrics)
    write_json(credit_dir / "metrics.json", credit_metrics)
    fraud_artifact["curve"].to_csv(fraud_dir / "threshold_curve.csv", index=False)
    credit_artifact["curve"].to_csv(credit_dir / "threshold_curve.csv", index=False)
    plot_cost_curve(
        fraud_artifact["curve"],
        fraud_dir / "cost_curve.png",
        "Fraud validation cost by threshold",
    )
    plot_cost_curve(
        credit_artifact["curve"],
        credit_dir / "cost_curve.png",
        "Credit validation cost by threshold",
    )

    psi = psi_table(
        fraud_artifact["reference_features"],
        fraud_artifact["current_features"],
        [col for col in SETTINGS.fraud_numeric if col in fraud_artifact["reference_features"].columns],
    )
    psi.to_csv(artifact_dir / "fraud_feature_psi.csv", index=False)
    report = render_monitoring_report(
        artifact_dir / "monitoring_report.md",
        fraud_metrics,
        credit_metrics,
        psi,
    )
    summary = _summary(fraud_metrics, credit_metrics)
    (artifact_dir / "evaluation_summary.md").write_text(summary, encoding="utf-8")
    _try_mlflow("fraud", fraud_metrics)
    _try_mlflow("credit", credit_metrics)
    logger.info("Training complete. Monitoring report written.")
    return {"fraud": fraud_metrics, "credit": credit_metrics, "report": report, "summary": summary}


def _train_one(
    frame: pd.DataFrame,
    time_col: str,
    train_end: str,
    valid_end: str,
    target: str,
    numeric: list[str],
    categorical: list[str],
    primary: str,
    baseline_scores: np.ndarray,
) -> tuple[dict, dict]:
    assert_no_leaky_columns(numeric + categorical)
    working = frame.copy()
    working["_baseline"] = np.asarray(baseline_scores, dtype=float)
    train, valid, test, method = split_for_training(working, time_col, train_end, valid_end, target)
    preprocessor = _preprocessor(numeric, categorical)
    x_train = preprocessor.fit_transform(train[numeric + categorical])
    x_valid = preprocessor.transform(valid[numeric + categorical])
    x_test = preprocessor.transform(test[numeric + categorical])
    y_train = train[target].to_numpy(dtype=int)
    y_valid = valid[target].to_numpy(dtype=int)
    y_test = test[target].to_numpy(dtype=int)

    candidates = _candidates(y_train)
    fitted = {}
    valid_scores = {}
    for name, model in candidates.items():
        model.fit(x_train, y_train)
        fitted[name] = model
        valid_scores[name] = model.predict_proba(x_valid)[:, 1]

    def _metric(scores: np.ndarray) -> float:
        value = safe_pr_auc(y_valid, scores) if primary == "pr_auc" else safe_roc_auc(y_valid, scores)
        return -1.0 if value is None else float(value)

    best_name = max(fitted, key=lambda name: _metric(valid_scores[name]))
    best = fitted[best_name]
    train_scores = best.predict_proba(x_train)[:, 1]
    calibrator = fit_platt(train_scores, y_train)
    valid_p = apply_platt(calibrator, valid_scores[best_name])
    test_p = apply_platt(calibrator, best.predict_proba(x_test)[:, 1])
    curve = threshold_cost_curve(
        y_valid,
        valid_p,
        fn_cost=SETTINGS.false_negative_cost,
        fp_cost=SETTINGS.false_positive_cost,
    )
    chosen = select_threshold(curve)
    review = float(chosen["threshold"])
    block = _block_threshold(valid_p, review)
    valid_metrics = classification_bundle(y_valid, valid_p, review)
    test_metrics = classification_bundle(y_test, test_p, review)
    decisions = decide(test_p, review, block)
    payload = {
        "split_method": method,
        "model_name": best_name,
        "calibration": "platt_on_training_scores" if calibrator is not None else "none",
        "primary_metric": primary,
        "review_threshold": review,
        "block_threshold": block,
        "validation_business_cost": float(chosen["business_cost"]),
        "baseline_valid_pr_auc": safe_pr_auc(y_valid, valid["_baseline"].to_numpy()),
        "baseline_valid_roc_auc": safe_roc_auc(y_valid, valid["_baseline"].to_numpy()),
        "valid": valid_metrics,
        "test": test_metrics,
        "test_decisions": {
            "approve": int((decisions == "approve").sum()),
            "review": int((decisions == "review").sum()),
            "block": int((decisions == "block").sum()),
        },
        "rows": {"train": int(len(train)), "valid": int(len(valid)), "test": int(len(test))},
    }
    artifact = {
        "preprocessor": preprocessor,
        "model": best,
        "calibrator": calibrator,
        "model_name": best_name,
        "numeric": numeric,
        "categorical": categorical,
        "review_threshold": review,
        "block_threshold": block,
        "target": target,
        "curve": curve,
        "reference_features": train[numeric].reset_index(drop=True),
        "current_features": test[numeric].reset_index(drop=True),
    }
    return payload, artifact


def _preprocessor(numeric: list[str], categorical: list[str]) -> ColumnTransformer:
    numeric_pipe = Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]
    )
    categorical_pipe = Pipeline(
        [
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        [
            ("num", numeric_pipe, numeric),
            ("cat", categorical_pipe, categorical),
        ]
    )


def _candidates(y_train: np.ndarray) -> dict:
    positive = max(int((y_train == 1).sum()), 1)
    negative = int((y_train == 0).sum())
    weight = negative / positive
    models: dict = {
        "logistic_regression": LogisticRegression(
            max_iter=400, class_weight="balanced", random_state=SETTINGS.seed
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=40,
            max_depth=6,
            min_samples_leaf=5,
            class_weight="balanced_subsample",
            random_state=SETTINGS.seed,
            n_jobs=1,
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            max_depth=3,
            max_iter=80,
            learning_rate=0.08,
            random_state=SETTINGS.seed,
        ),
    }
    try:
        from xgboost import XGBClassifier

        models["xgboost"] = XGBClassifier(
            n_estimators=80,
            max_depth=3,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=SETTINGS.seed,
            n_jobs=1,
            scale_pos_weight=weight,
        )
    except ImportError:
        logger.info("XGBoost is not installed; training logistic regression and gradient boosting.")
    return models


def _block_threshold(scores: np.ndarray, review_threshold: float) -> float:
    flagged = scores >= review_threshold
    if int(flagged.sum()) < 5:
        return float(min(0.99, review_threshold + 0.1))
    cutoff = float(np.quantile(scores[flagged], 0.80))
    return float(min(0.99, max(cutoff, review_threshold)))


def score_frame(artifact: dict, frame: pd.DataFrame) -> np.ndarray:
    columns = artifact["numeric"] + artifact["categorical"]
    matrix = artifact["preprocessor"].transform(frame.loc[:, columns])
    raw = artifact["model"].predict_proba(matrix)[:, 1]
    return apply_platt(artifact.get("calibrator"), raw)


def _summary(fraud_metrics: dict, credit_metrics: dict) -> str:
    fraud_text = _fraud_paragraph(fraud_metrics)
    credit_text = _credit_paragraph(credit_metrics)
    return "\n".join(
        [
            "# Evaluation summary",
            "",
            "Synthetic laboratory results. These numbers describe the generated book, not a live portfolio.",
            "",
            "## Fraud",
            "",
            fraud_text,
            "",
            "## Credit",
            "",
            credit_text,
            "",
        ]
    )


def _fraud_paragraph(metrics: dict) -> str:
    valid = metrics["valid"]
    model_pr = valid.get("pr_auc")
    base_pr = metrics.get("baseline_valid_pr_auc")
    if model_pr is None or base_pr is None:
        comparison = "Validation labels were too sparse for a stable PR-AUC comparison."
    elif model_pr > base_pr:
        comparison = (
            f"The selected model ({metrics['model_name']}) outranks the velocity and amount rule "
            f"on validation PR-AUC ({model_pr:.3f} versus {base_pr:.3f})."
        )
    else:
        comparison = (
            f"The velocity and amount rule matched or beat the model on validation PR-AUC "
            f"({base_pr:.3f} versus {model_pr:.3f}). I would keep the rule as the baseline."
        )
    recall = valid.get("recall") or 0.0
    precision = valid.get("precision") or 0.0
    return (
        "The objective is to catch fraudulent transactions without flooding investigators. "
        f"The unit is a transaction, the label is confirmed fraud, and the split is {metrics['split_method']}. "
        f"At validation threshold {metrics['review_threshold']:.3f}, recall is {recall:.1%} and "
        f"precision is {precision:.1%}. That point minimizes expected cost when a miss costs "
        f"${SETTINGS.false_negative_cost:.0f} and a false review costs ${SETTINGS.false_positive_cost:.0f}. "
        f"{comparison} "
        "I would shadow-score production traffic and watch investigator workload before automatic blocks. "
        "Retrain when feature PSI and the cost curve move together, not because accuracy twitched."
    )


def _credit_paragraph(metrics: dict) -> str:
    valid = metrics["valid"]
    auc = valid.get("roc_auc")
    ks = valid.get("ks")
    auc_text = "n/a" if auc is None else f"{auc:.3f}"
    ks_text = "n/a" if ks is None else f"{ks:.3f}"
    return (
        "The objective is to rank probability of default over 12 months from origination. "
        "Expected loss is PD x LGD x EAD; the classifier estimates PD only. "
        f"Validation ROC-AUC is {auc_text} and KS is {ks_text} using {metrics['model_name']} "
        f"on a {metrics['split_method']} split. "
        "I would not approve the maximum number of applicants the PD model can rank. "
        "The cutoff should be the one whose expected loss and approval rate the risk committee accepts, "
        "checked on a seasoned outcome window so recent originations are not treated as good loans."
    )


def _try_mlflow(name: str, metrics: dict) -> None:
    import os

    os.environ.setdefault("MLFLOW_DISABLE_AGENT_HINT", "1")
    try:
        import mlflow
    except ImportError:
        return
    try:
        tracking = SETTINGS.repo_root / "mlflow.db"
        mlflow.set_tracking_uri("sqlite:///" + tracking.resolve().as_posix())
        with mlflow.start_run(run_name=f"lab-{name}"):
            mlflow.log_param("model_name", metrics["model_name"])
            mlflow.log_param("split_method", metrics["split_method"])
            flat = {}
            for split in ("valid", "test"):
                for key, value in metrics[split].items():
                    if isinstance(value, (int, float)) and value == value:
                        flat[f"{split}_{key}"] = float(value)
            if flat:
                mlflow.log_metrics(flat)
    except Exception as exc:
        logger.warning("MLflow logging failed for %s (%s); training artifacts were still saved.", name, exc)
