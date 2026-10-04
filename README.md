# fintech-quant-data-scientist-interview

Quantitative Data Science • Risk • Fraud • ML • SQL • Spark • Snowflake • AWS • MLOps

A hands-on laboratory for a mid-level quantitative data scientist interview in financial technology, risk, fraud, and financial intelligence.

This repository is a **portfolio project** built on **synthetic data**. It is a simulated production environment and a technical demonstration. It is not a record of employment at a bank or a FinTech company, and it is not a claim of production fraud, production credit-risk, Snowflake, or AWS ownership.

## What the laboratory trains

Every model in the repository follows the same loop:

```text
BUSINESS PROBLEM → DATA → DATA QUALITY → EDA → FEATURE ENGINEERING
→ BASELINE → MODEL → VALIDATION → THRESHOLD / DECISION → BUSINESS COST
→ DEPLOYMENT → MONITORING → BUSINESS IMPACT
```

Accuracy is one number in that loop. The decision also needs a horizon, a unit of observation, a baseline, a cost for false positives and false negatives, a leakage check, a validation window, a deploy path, a monitor, and a reason to retrain.

## Quick start

```bash
python -m pip install -r requirements.txt
python scripts/generate_data.py --customers 1000 --transactions 10000
python scripts/train.py
python scripts/evaluate.py
pytest
python scripts/interview.py --topic sql
python scripts/interview.py --topic fraud
python scripts/interview.py --full
streamlit run app.py
```

Laptop-sized generation (the default in the Makefile) is 10,000 customers and 100,000 transactions. The full teaching scale is:

```bash
python scripts/generate_data.py --customers 100000 --transactions 5000000
```

The generator is seeded. The same seed reproduces the same book, including the deliberate defects: missing categories, duplicate ids, impossible ages, and a fraud-rate shift after 2025-06-01.

## How to use it in an interview

1. Solve an exercise from `python/` or `sql/` without opening `solution.py`.
2. Run `pytest` on that exercise.
3. Practice a spoken answer from `mock-interviews/question_bank.json`. Each important question has a 30-second answer, a 2-minute answer, a deep dive, follow-ups, and a common mistake.
4. Run `python scripts/interview.py --full` for a 90-minute agenda. The scorecard stays blank until you pass `--scores`. The tool does not invent your score.
5. For behavioral prompts, replace `[YOUR REAL EXAMPLE]`, `[YOUR ACTION]`, and `[YOUR RESULT]`. Do not borrow a story from this repository and present it as a job.

## Layout

| Path | Role |
| --- | --- |
| `src/` | Feature logic, training, metrics, scoring API |
| `scripts/` | Generate, train, evaluate, interview |
| `python/` | 150+ coding exercises with tests |
| `sql/` | 200+ financial SQL exercises, plus a performance track |
| `statistics/` | Inference examples and the statistics question bank |
| `fraud/`, `credit-risk/`, `customer-lifetime-value/` | Decision write-ups for the three models |
| `time-series/` | Forecasting and backtesting |
| `machine-learning/` | Validation, leakage, fairness diagnostics, optional PyTorch |
| `spark/`, `snowflake/`, `aws/`, `mlops/` | Scale and deployment labs that run locally |
| `system-design/`, `case-studies/`, `behavioral/` | Spoken interview practice |
| `capstone/` | Enterprise financial intelligence platform on one synthetic book |
| `docs/` | 12-week plan, requirement matrix, readiness checklist |

Production logic lives in `src/`. Notebooks call that library. They are not a second implementation.

## Stack

Python 3.11+, Pandas, NumPy, scikit-learn, XGBoost when installed, SQL, a local PostgreSQL schema, MLflow, FastAPI, Streamlit, Docker, pytest, Ruff, and Black.

PyTorch and PySpark are optional (`requirements-optional.txt`). Snowflake and AWS are documented architectures with local file and SQL stand-ins. Nothing in the default path needs a paid account.

## Decision costs used in the lab

| Outcome | Cost used for threshold selection |
| --- | --- |
| False negative (missed fraud or missed default, teaching matrix) | $500 |
| False positive (unnecessary review or decline) | $5 |

The threshold is chosen on the validation window only. The test window is scored once. HistGradientBoosting is the gradient-boosting candidate. Logistic regression, a random forest, and XGBoost (when installed) compete on the validation metric. Probabilities are Platt-scaled on training scores before that threshold is chosen.

## Philosophy

Don't just build a model. Understand the financial problem, build the right data pipeline, validate the model rigorously, quantify the business trade-offs, deploy it reliably, monitor it continuously, and communicate the decision clearly.
