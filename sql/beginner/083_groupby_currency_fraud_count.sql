-- fraud count by currency
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute the fraud count of transactions by currency. Return the group, the metric, and order by the metric descending.
--
-- Approach: Group by currency and aggregate. Keep the transaction count beside any rate so a small bucket cannot look precise.
-- Common mistake: Sorting groups by a rate without a minimum volume promotes tiny noisy buckets.

SELECT currency AS bucket,
       SUM(is_fraud) AS metric_value,
       COUNT(*) AS transactions
FROM transactions
GROUP BY currency
ORDER BY metric_value DESC;
