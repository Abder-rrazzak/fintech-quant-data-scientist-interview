-- fraud count by transaction_type
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute the fraud count of transactions by transaction_type. Return the group, the metric, and order by the metric descending.
--
-- Approach: Group by transaction_type and aggregate. Keep the transaction count beside any rate so a small bucket cannot look precise.
-- Common mistake: Sorting groups by a rate without a minimum volume promotes tiny noisy buckets.

SELECT transaction_type AS bucket,
       SUM(is_fraud) AS metric_value,
       COUNT(*) AS transactions
FROM transactions
GROUP BY transaction_type
ORDER BY metric_value DESC;
