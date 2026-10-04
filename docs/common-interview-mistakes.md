# Common interview mistakes

- Optimizing accuracy on a 0.1% fraud label.
- Quoting ROC-AUC when the operating point is a review queue. PR-AUC and cost belong next to it.
- A random split on transactions that share a customer or a future.
- Using `balance_after`, the fraud label, or a same-month aggregate as a feature.
- Tuning the threshold on the test window.
- Calling an outlier a fraud, or a fraud an outlier, with no overlap stated.
- A backtest that is a shuffled cross-validation.
- A p-value described as the probability that the null is true.
- "The model is fair" from a single rate gap, or a legal conclusion the data cannot support.
- Spark for a dataset that fits in memory, or Pandas for a join that does not.
- A Snowflake or AWS answer that is a product list and never mentions pruning, cost, or permissions.
- A system design that never names the fallback, the label delay, or the owner of the threshold.
- An email that starts with "AUC went up 0.05" and never says what to do.
