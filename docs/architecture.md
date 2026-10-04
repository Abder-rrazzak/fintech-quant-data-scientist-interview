# Architecture

The laboratory runs on files. Cloud products appear as optional production translations.

```text
synthetic generator
        │
        ▼
data/raw  (Parquet, with deliberate defects)
        │
        ▼
clean + point-in-time features   (src/features, src/data/quality.py)
        │
        ├── fraud model ── cost threshold ── approve / review / block
        ├── credit model ─ expected loss
        └── CLV / forecasts (separate targets and horizons)
        │
        ▼
artifacts/  +  MLflow run (best effort)
        │
        ├── FastAPI  serving.api:app
        ├── Streamlit app.py
        └── PSI monitoring report
```

## Feature store

`src/features/store.py` writes Parquet and reads with a backward as-of join. `snowflake/local/postgres_feature_store.sql` is the same idea in PostgreSQL. The online cache stores the latest value and is the thing that will skew if you score yesterday's decision with today's utilization.

## Why point-in-time correctness is critical

A default label looks 12 months forward. A fraud label arrives after investigation. If training joins the customer's current balance, current utilization, or a feature that includes the transaction you are scoring in its own baseline, the model studies a future it will not have in production. The validation number is then a fiction, and the gap shows up as soon as the service goes live.

## Batch and real-time translations

See `aws/README.md`. Locally, batch scoring is `aws/local_batch.py` and real-time scoring is the FastAPI process. Kafka, Kinesis, SageMaker, and Snowflake are named in the design answers and are not required to run the tests.
