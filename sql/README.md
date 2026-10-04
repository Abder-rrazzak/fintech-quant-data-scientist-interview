# SQL interview lab

At least 200 exercises under `beginner/`, `intermediate/`, `advanced/`, and `performance/`.

Each file states the question, an approach, and a common mistake. The dialect note is PostgreSQL / Snowflake-compatible teaching SQL. `tests/test_sql_patterns.py` runs the flagship patterns in SQLite:

- top 3 customers by month
- monthly transaction count up more than 50%
- consecutive fraudulent transactions

Window drills also include prior amount z-scores, rolling amounts, and the first transaction after a risk threshold. Read those files in `sql/advanced/`.

Performance walkthrough: `sql/performance/README.md`.
