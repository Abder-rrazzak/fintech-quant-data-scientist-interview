# Fraud rate rose from 0.15% to 0.35%.

Synthetic case for interview practice. Not a real portfolio incident.

## Clarifying questions

- What is the grain and the time window?
- Did the population, the label, or the feature contract change?
- What decision will this analysis change?

## Assumptions

- Costs and capacity are stated before a threshold is defended.
- Recent outcomes may be censored.
- This write-up does not assume access to a production warehouse.

## Analytical approach

Check mix, labeling, a new product, and a new attack before retraining. Compare rates within country, channel, and merchant category. If one slice explains the change, fix the slice. If the rate rose inside every major slice, then look at the model and the rules.

## Modeling approach

Only refit after the table, the label window, and the baseline are understood. Compare a simple rule or the current model on a later window.

## Metrics

Use the decision metric: cost, precision at capacity, approval versus seasoned loss. Report AUC or KS as supporting ranking evidence.

## Business trade-off

Name what gets worse if you chase the metric that got better. Ask who staffs the queue or who owns the loss.

## Recommendation

State the next action, the check that would reverse it, and what you will not do yet.
