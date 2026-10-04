# Spark

## 1. Business problem

Aggregate more transactions than a single machine should load, without changing the grain of the feature.

## 2. Dataset

The synthetic transactions. The unit test uses three rows. The generator can write five million.

## 3. Architecture

`spark/job.py`. `customer_daily_spend` is Pandas. `try_spark_daily_spend` runs the same aggregate with the DataFrame API when PySpark starts, and returns `None` when it cannot.

## 4. Data pipeline

Group by customer and calendar day. Sum amount. Count transactions. Sort so the result is comparable.

## 5. Feature engineering

Daily spend is an input to a later window, not a model by itself. A window in Spark must still exclude the future. Test that with a fixture, not with a plan screenshot.

## 6. Baseline

The Pandas aggregate. If Spark disagrees, Spark is wrong until you understand the cast of the timestamp.

## 7. Models

None in this module. Scoring a small model is a `mapInPandas` or a broadcast of the artifact, after the aggregate is trusted.

## 8. Validation

`tests/test_content.py` checks the Pandas path. A Spark session is optional and is not required for `pytest`.

## 9. Results

On a laptop extract, Spark startup can cost more than the aggregation. That is a result. Write it down.

## 10. Business interpretation

Use Spark when the join or the window does not fit, or when the data already lives there. Do not use it to feel production-ready.

## 11. Limitations

The optional path is a local master, not a cluster. Partitioning, skew, and broadcast size are interview topics in the question bank, not measured hardware results.

## 12. Production considerations

Predicate pushdown, a broadcast only when the dimension is small, salting for a hot key, and a schema check that fails the batch. `collect()` to the driver is a bug on this data.

## 13. Future improvements

A windowed 24-hour sum in Spark with an assertion that a future row does not enter the sum.
