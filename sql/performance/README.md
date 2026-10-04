# SQL performance

A slow analytical query is a plan problem before it is a hardware problem.

```text
BAD QUERY → EXPLAIN → BOTTLENECK → OPTIMIZED QUERY → COMPARISON
```

## A bad pattern

```sql
SELECT *
FROM transactions
WHERE date_trunc('month', timestamp) = DATE '2024-06-01'
  AND country = 'US';
```

Wrapping `timestamp` in `date_trunc` hides the range from the planner. `SELECT *` pulls columns the aggregate does not need. On a large table this becomes a scan.

## What you ask the plan

- How many rows enter the scan, and how many survive the filter?
- Is the join exploding because the grain is wrong?
- Is the aggregation shuffling a hot key?
- Is a function on the filter column blocking pruning?

## A clearer form

```sql
SELECT customer_id, SUM(amount) AS spend
FROM transactions
WHERE timestamp >= TIMESTAMP '2024-06-01'
  AND timestamp < TIMESTAMP '2024-07-01'
  AND country = 'US'
GROUP BY customer_id;
```

The predicate is a range. The select list is the aggregate. Compare scanned rows, not only clock time. Clock time moves when the warehouse is busy.

## What this lab expects you to name

| Lever | When it helps |
| --- | --- |
| Selective predicate | You can discard data before the join |
| Index or cluster on the filter column | The same range is the common query |
| Partition or micro-partition pruning | The filter matches the storage order |
| Pre-aggregate or materialized view | The same expensive group-by runs all day |
| Broadcast or replicate the small side | The dimension is actually small |
| Warehouse size | The plan is already honest and CPU-bound |

Exercises `sql/performance/053_bad_country_filter.sql` and `054_selective_predicate_first.sql` are the short drills. The advanced window queries are where the expensive plans usually hide: a window with no partition, or a join that duplicates transactions before the sum.
