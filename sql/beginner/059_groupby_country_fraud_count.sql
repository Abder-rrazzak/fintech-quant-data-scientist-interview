-- fraud count by country
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute the fraud count of transactions by country. Return the group, the metric, and order by the metric descending.
--
-- Approach: Group by country and aggregate. Keep the transaction count beside any rate so a small bucket cannot look precise.
-- Common mistake: Sorting groups by a rate without a minimum volume promotes tiny noisy buckets.

SELECT country AS bucket,
       SUM(is_fraud) AS metric_value,
       COUNT(*) AS transactions
FROM transactions
GROUP BY country
ORDER BY metric_value DESC;
