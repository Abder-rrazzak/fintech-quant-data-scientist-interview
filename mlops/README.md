# MLOps

## 1. Business problem

Know which model is serving, how it was trained, and when to stop trusting it.

## 2. Dataset

The synthetic raw extract and the artifacts under `artifacts/`.

## 3. Architecture

```text
Data → training → MLflow (best effort) → files as the registry
     → FastAPI → Docker → PSI monitoring
```

`src/pipelines/training.py` calls MLflow and still writes the joblib artifact if MLflow fails. The file is the source of truth for the API.

## 4. Data pipeline

`scripts/run_pipeline.py` generates a small book and trains. `docker-compose.yml` starts Postgres, the API, and the Streamlit app. The image is Python 3.11.

## 5. Feature engineering

The feature contract is `Settings.fraud_numeric` and `Settings.credit_numeric`. A break in those names is a failed release, not a silent null.

## 6. Baseline

The rule and the credit-score rank are stored as metrics next to the selected model. A release that hides them is incomplete.

## 7. Models

Joblib bundles the preprocessor, the model, the Platt map, the thresholds, and the feature frames used for PSI. The curve is for the report. Do not serve the curve.

## 8. Validation

`pytest` covers features, metrics, the API health check, and the 503 when the artifact is missing. A model test is the calendar split plus the leakage denylist.

## 9. Results

`artifacts/monitoring_report.md` and `artifacts/fraud_feature_psi.csv` after training. PSI bands of 0.10 and 0.25 are conventions documented in `src/monitoring/drift.py`.

## 10. Business interpretation

Drift in a feature is a prompt to look, not an automatic retrain. Performance drift needs matured labels. Until then, watch score quantiles and the decision mix.

## 11. Limitations

CI is described here and is not a hosted pipeline in this repository. MLflow's tracking directory is local (`mlruns/`).

## 12. Production considerations

Tests, logs, a versioned artifact, a health check, and an owner for the threshold. Retrain when the label definition changes, when PSI stays high and the later-window cost worsens, or on a schedule you can name. Do not retrain because a dashboard moved for one day.

## 13. Future improvements

A test that loads the joblib artifact and scores a fixture row, so a preprocessor mismatch fails in CI.
