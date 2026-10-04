# Anomaly lab

An outlier is a point that is unusual under a reference. Fraud is a business label. The sets overlap. A large genuine payroll wire is often an outlier. A low-and-slow fraud pattern may never be one.

## 1. Business problem

Find transactions worth a look when you do not yet trust the label, without blocking every large legitimate client.

## 2. Dataset

The same synthetic transactions. Use customer-level history, not one global fence, when the segments differ in size.

## 3. Architecture

`src/fraud/anomaly.py`: z-score, IQR, isolation forest, one-class SVM, local outlier factor, and a PCA reconstruction error as a linear autoencoder concept.

## 4. Data pipeline

Fit the reference on a past window. Score the next window. Do not fit the reference on the point you are scoring.

## 5. Feature engineering

Amount versus the customer's own history, and the same velocity features as the supervised model. Document the window so train and serve match.

## 6. Baseline

A z-score above 3, or an IQR fence at 1.5. Both are starting points. The review capacity is the real cutoff.

## 7. Models

Isolation forest, one-class SVM, and local outlier factor are unsupervised. Contamination changes the flag rate. It is not the fraud rate.

## 8. Validation

On a labeled slice, report the share of flags that are confirmed fraud and the share of fraud that was never flagged. Do not report accuracy.

## 9. Results

Unit tests in `tests/test_core.py` cover the z-score, IQR, and PCA residual on small arrays. They are fixtures, not a portfolio metric.

## 10. Business interpretation

A false anomaly block costs a genuine customer. Price that before you automate the block. Keep a rule in front when the pattern is already a sentence, such as three countries in an hour.

## 11. Limitations

PCA reconstruction is a teaching stand-in for an autoencoder. It is linear. A deep autoencoder is justified only if it beats this residual on a later window.

## 12. Production considerations

Log the reference window, the score, and the extreme features. A binary flag with no context cannot be audited.

## 13. Future improvements

Segment the reference so corporate clients are not flagged for being large.
