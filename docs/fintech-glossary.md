# FinTech glossary

Teaching definitions for this laboratory. They are not legal or regulatory definitions.

| Term | Meaning in this lab |
| --- | --- |
| Authorization | The transaction decision. The grain of the fraud model. |
| PD | Probability of default over a stated horizon. Here, 12 months from origination. |
| LGD | Loss given default, as a fraction of exposure. A modeling assumption in `src/risk/expected_loss.py`. |
| EAD | Exposure at default. Here, the loan principal on the synthetic loan. |
| Expected loss | PD × LGD × EAD. A teaching identity, not a Basel capital number. |
| Chargeback / dispute | A later label. It is not known at authorization time. |
| MCC | Merchant category. Some categories are marked high-risk in the generator. They are still not proof of fraud. |
| Velocity | Count or amount in a trailing window. Windows in this lab include the current row only when the docstring says so. |
| Point-in-time | A feature uses only rows whose timestamp is knowable at the decision. |
| Vintage | Loans grouped by origination period. A young vintage is censored. |
| KS | The maximum gap between the cumulative goods and bads. A ranking summary, not a decision. |
| PSI | Population stability index. A shift in a distribution. The 0.10 and 0.25 bands are conventions, not laws. |
| Review / block | Two thresholds. Review spends a person. Block spends a customer. |
| Basis point | 0.01 percentage point, or 1/100 of a percent. Used for transaction-cost assumptions in the backtest. |
