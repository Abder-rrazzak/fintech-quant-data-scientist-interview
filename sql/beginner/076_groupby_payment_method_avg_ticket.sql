-- average ticket by payment_method
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute the average ticket of transactions by payment_method. Return the group, the metric, and order by the metric descending.
--
-- Approach: Group by payment_method and aggregate. Keep the transaction count beside any rate so a small bucket cannot look precise.
-- Common mistake: Sorting groups by a rate without a minimum volume promotes tiny noisy buckets.

SELECT payment_method AS bucket,
       AVG(amount) AS metric_value,
       COUNT(*) AS transactions
FROM transactions
GROUP BY payment_method
ORDER BY metric_value DESC;
