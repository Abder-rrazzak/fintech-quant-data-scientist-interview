# Customer lifetime value

## 1. Business problem

Rank customers by the value you can still influence, so acquisition and retention spend has a denominator.

## 2. Dataset

Synthetic transactions and customers. Revenue after a cutoff is the label. Features stop at the cutoff.

## 3. Architecture

`src/models/clv.py`: RFM table, a simple margin-times-retention CLV, a horizon revenue frame, and a histogram gradient boosting regressor.

## 4. Data pipeline

`horizon_revenue_frame` builds features from transactions before the cutoff and revenue from transactions after it.

## 5. Feature engineering

Recency, frequency, monetary value, and the segment already on the customer. Do not use revenue from the horizon as a feature.

## 6. Baseline

`simple_clv`: average order value times a purchase frequency times a margin, discounted. The docstring states the formula.

## 7. Models

The simple identity, the gradient-boosting regressor on pre-cutoff features, and a note that a probabilistic BG/NBD model is a different estimator. This lab does not fit BG/NBD.

## 8. Validation

Fit on customers observed before the cutoff. Score revenue after the cutoff. A random split of transactions leaks the horizon into the features.

## 9. Results

`notebooks/04_customer_lifetime_value.ipynb` calls the library. Quote the error in currency, on the held-out horizon.

## 10. Business interpretation

Use the ranking to decide who receives a retention offer. A model that only rediscovers last month's spend will look accurate and will not change the decision.

## 11. Limitations

The generator's spend process is simpler than a real retention curve. There is no margin table beyond the assumption inside `simple_clv`.

## 12. Production considerations

Refresh the cutoff on a schedule. Monitor the mix of recency so a campaign that changes behavior is visible as drift, not as a silent win.

## 13. Future improvements

A contractual probabilistic model, with the same horizon discipline, compared on currency error rather than on in-sample likelihood.
