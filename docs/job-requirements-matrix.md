# Job requirements matrix

Every row is something a mid-level quantitative data scientist interview in risk, fraud, or financial intelligence actually asks. The counts below are floors. The question bank is larger.

| Job requirement | Repository module | Practical project | Interview questions |
| --- | --- | --- | --- |
| Predictive modeling | `machine-learning/`, `src/pipelines/training.py` | Credit risk model | 30+ in topic `predictive_modeling` |
| Fraud detection | `fraud/`, `src/features/transactions.py`, `src/fraud/` | Fraud engine with approve / review / block | 30+ in topic `fraud` |
| Anomaly detection | `fraud/anomaly/`, `src/fraud/anomaly.py` | Anomaly lab. Outlier is not fraud | 20+ in topic `anomaly` |
| Customer lifetime value | `customer-lifetime-value/`, `src/models/clv.py` | RFM, simple CLV, predictive CLV | 15+ in topic `clv` |
| SQL | `sql/beginner`, `sql/intermediate`, `sql/advanced` | Transaction analytics, including month-over-month volume | 100+ in topic `sql`, 200+ exercises |
| Pandas | `python/` topic `pandas`, `src/features/` | Feature engineering on transactions | 50+ in topic `pandas` |
| NumPy | `python/` topic `numpy` | Numerical lab, vectorized costs and returns | 30+ in topic `numpy` |
| Python | `python/beginner`, `python/intermediate`, `python/advanced` | Coding exercises with tests | 40+ spoken, 150+ exercises |
| Time series | `time-series/`, `src/forecasting/series.py` | Train 2020–2023, validate 2024, test 2025 | 30+ in topic `time_series` |
| Backtesting | `time-series/backtesting/`, `src/forecasting/backtest.py` | Expanding and rolling windows, costs, slippage | 20+ in topic `backtesting` |
| Spark | `spark/job.py` | Daily customer spend, Pandas fallback | 30+ in topic `spark` |
| Snowflake | `snowflake/` | Warehouse lab with PostgreSQL stand-in | 30+ in topic `snowflake` |
| AWS | `aws/` | Batch and real-time architecture, local scorer | 30+ in topic `aws` |
| Model validation | `machine-learning/validation/` | Calendar splits, grouped splits, leakage tests | 30+ in topic `validation` |
| Statistical bias and fairness | `machine-learning/bias/`, `statistics/` | Group approval gaps, hypothesis tests | 20+ bias, 100+ statistics |
| Cross-functional communication | `case-studies/business-communication/` | Thirty rewrites from metric to decision | 30+ in topic `business` |
| System design | `system-design/` | Fraud, credit, feature store, monitoring | 30 designs |
| MLOps and monitoring | `mlops/`, `src/monitoring/` | MLflow, FastAPI, PSI report | Covered in AWS, validation, and system design |
| Credit risk | `credit-risk/`, `src/risk/expected_loss.py` | PD, LGD, EAD, expected loss | 20+ in topic `credit_risk` |

The spoken bank is `mock-interviews/question_bank.json`. `tests/test_content.py` fails if a floor is missed.
