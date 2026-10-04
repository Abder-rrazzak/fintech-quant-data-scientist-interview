# Fraud engine

Synthetic laboratory. Not a production fraud system and not a claim of employment.

## 1. Business problem

Decide, for each authorization, whether to approve, review, or block, under a limited review queue.

## 2. Dataset

`scripts/generate_data.py` writes transactions with velocity, geography, device, and a rare `is_fraud` label. The generator also injects duplicates and missing fields. A fraud-rate shift starts on 2025-06-01.

## 3. Architecture

Transaction → point-in-time features → score → validation threshold → approve / review / block → PSI report. Code: `src/features/transactions.py`, `src/pipelines/training.py`, `src/fraud/decisions.py`.

## 4. Data pipeline

`clean_transactions` drops duplicate ids, null keys, negative purchases, and impossible ages. Raw defects stay in `data/raw` so the quality report still sees them.

## 5. Feature engineering

Inclusive 1-hour and 24-hour counts. Amount z-score uses the mean and standard deviation strictly before the current row. `new_device` is the first time that device is seen for the customer. `geo_mismatch` compares the transaction country with the customer's home country. `is_fraud`, `balance_after`, and `detected_at` are banned.

## 6. Baseline

`fraud_rule_score`: a weighted combination of amount z-score, 1-hour velocity, geo mismatch, and a new device.

## 7. Models

Logistic regression, random forest, histogram gradient boosting, and XGBoost when it is installed. The validation PR-AUC picks the candidate. Training scores are Platt-scaled before the threshold.

Unsupervised scores live in `src/fraud/anomaly.py` and are not treated as the fraud label.

## 8. Validation

Train through 2024-12-31, validate through 2025-06-01, test after that (the drift window). If a bucket is too small, the code falls back to a time-ordered quantile split and labels it `time_quantile_fallback`. There is no random split.

## 9. Results

Written to `artifacts/fraud/metrics.json` and `artifacts/evaluation_summary.md` after `python scripts/train.py`. Those numbers describe the synthetic book only. The summary says so when the baseline wins.

## 10. Business interpretation

False negative cost is $500 and false positive cost is $5 in the teaching matrix. The review threshold minimizes validation cost. The block threshold is the 80th percentile of scores already above review.

## 11. Limitations

The label is generated from the same signals the features use, so the problem is easier than a live book. Investigation delay is simulated, not observed. The cost matrix is an assumption.

## 12. Production considerations

Serve `score_frame` from the FastAPI app. Log the model version, the score, and the decision. Fall back to the rule if the artifact or a feature is missing. Do not retrain during an outage that looks like fraud.

## 13. Future improvements

Separate card-testing, account-takeover, and friendly-fraud labels. Add a capacity constraint so the threshold cannot enqueue more reviews than the team can finish.
