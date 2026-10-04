-- total spend by customer_segment
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute the total spend of transactions by customer_segment. Return the group, the metric, and order by the metric descending.
--
-- Approach: Group by customer_segment and aggregate. Keep the transaction count beside any rate so a small bucket cannot look precise.
-- Common mistake: Sorting groups by a rate without a minimum volume promotes tiny noisy buckets.

SELECT customer_segment AS bucket,
       SUM(amount) AS metric_value,
       COUNT(*) AS transactions
FROM transactions
GROUP BY customer_segment
ORDER BY metric_value DESC;
