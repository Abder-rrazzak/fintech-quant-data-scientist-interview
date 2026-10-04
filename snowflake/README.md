# Snowflake lab

No Snowflake account is required. The SQL habits below are practiced on PostgreSQL and on the files in `sql/`.

## 1. Business problem

Answer analytical questions on a large transaction table without scanning it all, and without surprising the warehouse bill.

## 2. Dataset

The synthetic Parquet extract. Loading it is a local `COPY` equivalent: `\copy` in PostgreSQL, or `pandas.read_parquet` in the lab.

## 3. Architecture

Virtual warehouses are compute. Databases and schemas are namespaces. Stages are places files land before `COPY INTO`. Streams and tasks move increments. Time Travel lets you read a previous version. Clustering and micro-partition pruning decide how much a filter reads.

## 4. Data pipeline

Land files, copy them in, transform in SQL (ELT). Make the transform idempotent so a retry does not double a day. `snowflake/local/postgres_feature_store.sql` is the feature-table version of that idea.

## 5. Feature engineering

An as-of lookup is the latest feature row at or before the decision time. The index is `(customer_id, event_time DESC)`.

## 6. Baseline

The same query on a sample in SQLite or Postgres. Promote the SQL after the numbers match. Dialect differences get written down, not discovered in production.

## 7. Models

None. The warehouse is where you build the training table. Fitting stays in `src/pipelines/training.py`.

## 8. Validation

Compare row counts and a few aggregates between the sample engine and the warehouse SQL. A green job that doubled the grain is not a success.

## 9. Results

`tests/test_sql_patterns.py` executes the top-3, month-over-month, and consecutive-fraud patterns in SQLite.

## 10. Business interpretation

Credits follow warehouse size and how long it stays on. Auto-suspend matters. A dashboard that polls every minute will keep a warehouse awake.

## 11. Limitations

This repository does not connect to Snowflake. Answers that only list product names miss the point. The point is pruning, isolation of compute, and idempotent increments.

## 12. Production considerations

Separate roles for loading and for reading. Tag queries so a credit spike maps to a statement. Do not wrap a timestamp filter in a function if you want pruning.

## 13. Future improvements

A Postgres compose service is already declared in `docker-compose.yml`. Apply the feature-store SQL there when you want a server rather than a file.
