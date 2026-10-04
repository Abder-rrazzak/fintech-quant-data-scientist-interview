# Bias and fairness diagnostics

These measurements are not a legal conclusion. Whether a disparity is unlawful depends on jurisdiction, the decision, and facts this laboratory does not have.

## 1. Business problem

See whether two groups receive different approval rates or different true-positive rates, and separate mix from a residual gap.

## 2. Dataset

Any scored frame with a group column. The synthetic generator has `customer_segment`. Segment is not a protected class. Treat the exercise as a measurement drill.

## 3. Architecture

`src/evaluation/fairness.py` and `machine-learning/bias/compare_groups.py`.

## 4. Data pipeline

Compute rates with counts. A rate on 30 people is a noisy rate.

## 5. Feature engineering

A proxy you do not understand is not a protected-class analysis. Do not invent one.

## 6. Baseline

The overall approval rate, then the rate inside score bands. A raw gap can be mix.

## 7. Models

Demographic parity difference is the gap in selection rates. Equal opportunity difference is the gap in true positive rates. They can disagree. Forcing one of them has a loss consequence. Show that consequence.

## 8. Validation

Use matured labels for error-rate gaps. A recent vintage has not defaulted yet.

## 9. Results

Report the table from `approval_table` with `n` beside every rate. Do not summarize it as "the model is fair."

## 10. Business interpretation

If true risk differs and you force equal approvals, you accept more loss in one group or decline good applicants in another. That trade-off is a policy choice. Name it. Do not hide it in a metric.

## 11. Limitations

Sampling bias, selection bias, measurement bias, survivorship, and label bias (one group is reviewed more, so the label is more complete) are all possible and none of them is identified by a single gap.

## 12. Production considerations

Document which slices were measured, the counts, and the metric. Retrain does not remove a biased label.

## 13. Future improvements

A score-banded comparison so mix and residual gap are visible on the same page.
