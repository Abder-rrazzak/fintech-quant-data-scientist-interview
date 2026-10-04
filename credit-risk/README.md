# Credit risk

Synthetic laboratory. Not a production credit book and not a claim of employment.

## 1. Business problem

Estimate the 12-month probability of default at origination, then choose an approval cutoff that prices missed defaults against declined good applicants.

## 2. Dataset

`loans` carries the application snapshot: income, score, utilization, debt-to-income, delinquencies, employment, principal, rate. `default_12m` is the target. Loans are originated only through 2024-12-31 so the horizon can be observed inside the generator's calendar.

## 3. Architecture

Application features plus transaction history strictly before origination → candidate models → Platt scaling → cost threshold → expected loss = PD × LGD × EAD.

## 4. Data pipeline

`attach_credit_transaction_features` uses a searchsorted window that ends before origination. A future purchase cannot enter `txn_count_90d`.

## 5. Feature engineering

Income, credit score, utilization, debt-to-income, account age, prior delinquency count, principal, interest rate, 90-day transaction count, and 90-day average amount. Employment status and segment are categorical. `default_12m` is banned as a feature.

## 6. Baseline

`(850 - credit_score) / 550`, clipped to `[0, 1]`. The model has to beat this rank on the validation window.

## 7. Models

Logistic regression, random forest, histogram gradient boosting (the gradient-boosting candidate), and XGBoost when installed. Selection metric is validation ROC-AUC. Probabilities are Platt-scaled on training scores. Metrics: ROC-AUC, PR-AUC, KS, precision, recall, F1, Brier, and the cost curve.

## 8. Validation

Originations through 2023-12-31 train, through 2024-06-30 validate, and the rest of 2024 tests. Young vintages are not labeled as non-defaults.

## 9. Results

`artifacts/credit/metrics.json` after training. Read it next to the baseline AUC in the same file. Expected loss for a single loan is `expected_loss(pd, lgd, ead)` in `src/risk/expected_loss.py`.

## 10. Business interpretation

A higher approval rate with a higher default rate can raise expected loss. The cutoff is a loss decision, not an accuracy decision. Reason codes, if you add them, have to be stable enough to show an applicant.

## 11. Limitations

LGD is a column on the synthetic loan, not a recovered-loss model. The teaching cost matrix is shared with fraud and is an assumption. This is not a regulatory capital calculation.

## 12. Production considerations

The policy cutoff lives outside the weights so risk can move it without a retrain. Bureau attributes that arrive after the decision are for monitoring, not for rewriting the score you already gave.

## 13. Future improvements

A separate LGD model, a documented reason-code list, and a calibration check on a seasoned vintage that was not used to fit Platt.
