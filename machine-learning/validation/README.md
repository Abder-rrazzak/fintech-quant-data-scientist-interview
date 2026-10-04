# Validation lab

## 1. Business problem

Trust a number only if the split matches the decision time and the features were knowable then.

## 2. Dataset

Fraud and credit frames from the synthetic book. The leakage fixtures in `leakage_examples.py` are tiny on purpose.

## 3. Architecture

`src/evaluation/validation.py`: calendar split, time-ordered quantile fallback, leakage denylist, point-in-time assertion.

## 4. Data pipeline

A customer-month mean computed on the whole month and copied onto every row is leakage. `future_mean_attached_to_the_past` builds that mistake so you can see it.

## 5. Feature engineering

Banned exact names include `is_fraud`, `default_12m`, and `balance_after`. `prior_delinquency_count` is allowed. The denylist does not substring-match the word "default".

## 6. Baseline

A shuffled-label model should look useless. If it still looks good, the pipeline is leaking. That negative control is the sanity check to add when you extend training.

## 7. Models

The training script compares logistic regression, a random forest, histogram gradient boosting, and XGBoost. Hyperparameter search belongs inside the training window. Grid search on the test window is leakage of a different kind.

## 8. Validation

Use a stratified split only when rows are independent and time does not matter. Use GroupKFold when rows share a customer. Use TimeSeriesSplit or the calendar split when time matters. Nested cross-validation is for the tuning loop, with a final later window held out.

## 9. Results

`split_method` in the metrics JSON is either the calendar design or `time_quantile_fallback`. Read it before you quote the AUC.

## 10. Business interpretation

A threshold is part of the model. Recompute the cost curve on a later month. If the old threshold's cost jumped, it aged.

## 11. Limitations

The fallback split exists so a tiny laptop sample still trains. It is not the production design. The metrics JSON names it.

## 12. Production considerations

Freeze the test dates before you look. If you look, the next window is the test.

## 13. Future improvements

A grouped split by customer inside the training window, plus the calendar holdout, for features that are pure customer history.
