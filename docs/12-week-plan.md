# 12-week interview plan

Each week has theory, coding, SQL, a project slice, interview questions, and a short mock. Stay on the synthetic book. When a prompt asks for a story from work, use your own and the placeholders in `behavioral/`.

## Week 1 — Python

- Theory: complexity, mutability, generators, errors, typing.
- Coding: `python/beginner`, then ten intermediate problems.
- SQL: `sql/beginner` filters and aggregations.
- Project: read `src/data/generate.py` far enough to name every table.
- Questions: `python scripts/interview.py --topic python --difficulty beginner`
- Mock: 20 minutes, explain one solution out loud.

## Week 2 — Pandas and NumPy

- Theory: vectorization, copies versus views, categorical dtypes, chunking.
- Coding: every `pandas` and `numpy` exercise.
- SQL: joins between customers, accounts, and transactions.
- Project: `notebooks/01_eda_financial_transactions.ipynb`.
- Questions: why `apply` loses to a vectorized column, and how you would stream a CSV larger than memory.
- Mock: optimize a groupby that builds customer features. Say what you would not load.

## Week 3 — SQL

- Theory: grain, joins that duplicate rows, NULL, CASE.
- Coding: a Pandas equivalent of one SQL aggregate, to prove you know the grain.
- SQL: `sql/intermediate`, including top 3 customers by month.
- Project: load `data/sample/transactions_sample.csv` and reproduce one query by hand.
- Questions: `python scripts/interview.py --topic sql`
- Mock: 15 minutes, one window function, spoken.

## Week 4 — Advanced SQL and performance

- Theory: `sql/performance/README.md`. Bad query, explain, bottleneck, rewrite.
- Coding: none beyond fixing your own SQL.
- SQL: consecutive fraud, prior z-scores, rolling 7-day and 30-day amounts.
- Project: month-over-month volume up more than 50%, with gaps handled explicitly.
- Questions: partitioning, clustering, predicate pushdown.
- Mock: the interviewer says the query is slow. You ask for the plan before you add an index.

## Week 5 — Statistics

- Theory: `statistics/README.md` and the worked script.
- Coding: confidence interval, two-proportion z-test, bootstrap mean.
- SQL: fraud rate by segment, with counts next to rates.
- Project: fraud rate moves from 0.15% to 0.35%. Compute an interval before you tell a story.
- Questions: `python scripts/interview.py --topic statistics`
- Mock: explain a p-value without saying "the probability the null is true."

## Week 6 — Machine learning

- Theory: baseline, split, metric, calibration.
- Coding: `machine-learning/validation/leakage_examples.py`.
- SQL: a feature that would leak if the window included the future. Write the safe version.
- Project: `notebooks/02_credit_risk.ipynb` after `scripts/train.py`.
- Questions: ROC-AUC versus PR-AUC, and when each one is the wrong headline.
- Mock: a model with AUC 0.90 that uses `balance_after`. Reject it.

## Week 7 — Fraud and anomaly detection

- Theory: `fraud/README.md` and `fraud/anomaly/README.md`.
- Coding: velocity, amount z-score, new device. Tests already exist in `tests/test_core.py`.
- SQL: consecutive suspicious transactions.
- Project: `notebooks/03_fraud_detection.ipynb`. Read the cost curve in `artifacts/fraud/` after training.
- Questions: `python scripts/interview.py --topic fraud`
- Mock: 0.1% fraud. You refuse accuracy and you price a false positive.

## Week 8 — Credit risk and CLV

- Theory: PD, LGD, EAD, expected loss. RFM versus a predictive CLV.
- Coding: `src/risk/expected_loss.py`, `src/models/clv.py`.
- SQL: first transaction after a risk score crosses a threshold.
- Project: `notebooks/02_credit_risk.ipynb`, `notebooks/04_customer_lifetime_value.ipynb`.
- Questions: topics `credit_risk` and `clv`.
- Mock: approval rate up, default rate up. You do not celebrate the approval rate.

## Week 9 — Time series and backtesting

- Theory: look-ahead, survivorship, concept drift.
- Coding: log returns, ACF, a causal expanding window.
- SQL: a 30-day rolling sum that does not use rows after the as-of date.
- Project: `time-series/` and `time-series/backtesting/`.
- Questions: topics `time_series` and `backtesting`.
- Mock: someone proposes a random train/test split on daily spend. You replace it with origins.

## Week 10 — Spark, Snowflake, AWS

- Theory: when a warehouse or a cluster is the wrong tool.
- Coding: `spark/job.py` on a small frame. Compare the Pandas result.
- SQL: the PostgreSQL feature-store query in `snowflake/local/`.
- Project: redraw `aws/README.md` from memory, then check it.
- Questions: one Spark shuffle, one Snowflake prune, one IAM boundary.
- Mock: "we should put this 200 MB aggregate on Spark." You say no, and why.

## Week 11 — MLOps and system design

- Theory: `mlops/README.md`, feature freshness, training-serving skew.
- Coding: hit `GET /health` and `POST /score/fraud` with the FastAPI app.
- SQL: an as-of join, latest row at or before the decision.
- Project: one design from `system-design/`, written in the required order.
- Questions: `python scripts/interview.py --topic system_design`
- Mock: 15 minutes, real-time fraud, including the fallback when the feature store times out.

## Week 12 — Mocks and capstone

- Theory: `docs/interview-strategy.md` and `docs/common-interview-mistakes.md`.
- Coding: one exercise you have not seen, timed.
- SQL: one exercise you have not seen, timed.
- Project: `python capstone/run_platform.py`, then read `capstone/run_notes.md`.
- Questions: `python scripts/interview.py --full`
- Mock: fill the scorecard yourself with `--scores`. Revise the weakest two topics. Use `docs/final-readiness-checklist.md`.
