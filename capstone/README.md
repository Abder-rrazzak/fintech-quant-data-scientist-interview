# Capstone — Enterprise financial intelligence platform

Synthetic laboratory. Snowflake and AWS are optional production translations in `snowflake/` and `aws/`. This run uses local files.

## 1. Business problem

One transaction stream feeds a credit decision, a fraud decision, and a lifetime-value view, with a shared feature discipline and a monitor.

## 2. Dataset

`python capstone/run_platform.py` generates 300 customers and 4,000 transactions under `capstone/data` so it does not overwrite `data/raw`.

## 3. Architecture

```text
TRANSACTIONS → INGESTION → DATA WAREHOUSE (Parquet / optional Postgres)
    → FEATURE ENGINEERING
    → CREDIT | FRAUD | CLV
    → RISK ENGINE (thresholds and expected loss)
    → MODEL SERVING (FastAPI) → DASHBOARD (Streamlit) and ALERTS (decision log)
    → MONITORING (PSI report)
```

## 4. Data pipeline

Generate, write Parquet, clean inside training, engineer point-in-time features, fit, save artifacts under `capstone/artifacts`.

## 5. Feature engineering

Shared windows in `src/features`. Fraud and credit do not share a label, a horizon, or a metric.

## 6. Baseline

Fraud rule score and the credit-score rank. CLV uses `simple_clv` when you run that notebook on the same book.

## 7. Models

The training script's candidates, plus the optional PyTorch module and the optional Spark aggregate. SQL patterns are the warehouse view of the same book.

## 8. Validation

Calendar splits inside `run_training`. Read `split_method` in the metrics. The capstone does not add a second, looser split.

## 9. Results

`capstone/run_notes.md` after a run. It quotes the raw fraud rate and the evaluation summary. Those numbers are the synthetic book.

## 10. Business interpretation

The risk engine is the thresholds and the expected-loss identity, not a third black-box model. Product and risk disagree by moving the threshold. Show the cost curve when they do.

## 11. Limitations

The small capstone book can fall back to a quantile time split when a calendar bucket is thin. The notes include the training summary, which names the split. It is still synthetic.

## 12. Production considerations

Docker Compose brings up Postgres, the API, and Streamlit. The API reads `artifacts/` at the repository root unless you point it at `capstone/artifacts`. Do not confuse the two directories.

## 13. Future improvements

A single decision log that joins fraud action, credit action, and a CLV band for the same customer, each with its own version.
