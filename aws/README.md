# AWS architecture lab

The diagrams are the interview answer. The executable path is local files. No AWS account is used, and this is not professional AWS experience.

## 1. Business problem

Train on history, score a decision, and keep a log you can replay, with permissions that cannot rewrite that history.

## 2. Dataset

`data/raw` stands in for a bucket. `artifacts/` stands in for a model object. The decision log is a CSV from `aws/local_batch.py`.

## 3. Architecture

### Batch

```text
S3 (data/raw)
  → Glue / Spark (spark/job.py or Pandas)
  → feature engineering (src/features)
  → training (src/pipelines/training.py)
  → model registry (artifacts/ and MLflow)
  → API (src/serving/api.py)
  → monitoring (src/monitoring)
```

### Real-time fraud

```text
Transaction
  → API
  → Kafka or Kinesis (a queue you would add; the lab calls the API directly)
  → stream processing
  → feature store (src/features/store.py)
  → model
  → decision engine (src/fraud/decisions.py)
  → alert
```

S3, EC2, Lambda, RDS, Redshift, Glue, Athena, SageMaker, CloudWatch, IAM, and VPC are the managed pieces you would name. Locally they collapse to files, a Python process, Postgres optional, and logs.

## 4. Data pipeline

`score_batch` engineers features, scores with the saved artifact, and writes transaction id, score, decision, and model name.

## 5. Feature engineering

The same point-in-time functions as training. A batch rebuild of history must use data available at each event, not today's snapshot.

## 6. Baseline

The rule score, logged beside the model score when you extend the log. The dashboard already shows both.

## 7. Models

Whatever `scripts/train.py` selected. The object name should include the version. Overwriting `latest` destroys rollback.

## 8. Validation

A fixture event, a missing artifact (the API returns 503), and a feature that fails the contract. `tests/test_core.py` covers the 503.

## 9. Results

The decision log is the result. Counts of approve, review, and block should match the threshold story.

## 10. Business interpretation

Shadow the new model before it can block anyone. A 50% canary on day one of a new block rule is how you create an incident.

## 11. Limitations

There is no network, no IAM simulator, and no stream broker in the default tests. Saying "VPC" is not a security design. The scorer's identity can read the model and the features, and cannot rewrite training data.

## 12. Production considerations

Alarm on queue lag, feature age, score quantiles, and decision mix. Put a timeout on training. Log ids, version, score, decision, and latency. Leave the full sensitive payload out of the log when you can.

## 13. Future improvements

A local queue in front of the API so the real-time diagram has a buffer you can stop and replay.
