# Project plan

Portfolio laboratory for a mid-level quantitative data scientist interview in FinTech, risk, fraud, and financial intelligence.

This repository is a **simulated production environment** built on **synthetic data**. It is not a description of employment, and it does not claim production ownership of a bank, card-network, fraud, credit, Snowflake, or AWS system.

## Build order

1. Inspect the parent workspace and leave unrelated files in place.
2. Scaffold packaging, containers, and documentation.
3. Implement the synthetic data platform and the reusable library under `src/`.
4. Implement training, evaluation, monitoring, serving, and the mock-interview CLI.
5. Materialize Python labs, SQL labs, statistics, case studies, and interview banks with executable checks.
6. Run `pytest`, then the generate / train / evaluate / interview commands, and fix failures before calling the lab complete.

## Business loop

Every model in this lab is judged with the same loop:

business problem, data, data quality, EDA, features, baseline, model, validation, threshold, business cost, deployment, monitoring, business impact.

Accuracy is never the only decision metric.

## Runtime choices

- Laptop path: `python scripts/generate_data.py --customers 10000 --transactions 100000`
- Interview-scale path: `python scripts/generate_data.py --customers 100000 --transactions 5000000`
- Validation path used in this build: `--customers 1000 --transactions 10000`
- Calendar time splits are the default. A time-ordered quantile split is used only when a small sample would leave a calendar bucket empty. That fallback is still not a random split.
- PyTorch and PySpark are implemented and optional to install, so the core lab runs without Java or a GPU.

## Out of scope

- Proprietary financial data
- Paid Snowflake or AWS accounts
- Fabricated personal employment stories in `behavioral/`
