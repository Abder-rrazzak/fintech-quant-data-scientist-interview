-- Customers with at least 10 fraud labels
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Return customers whose fraud-labeled transaction count is at least 10.
--
-- Approach: Filter to the label, aggregate to the customer, and use HAVING for the count threshold.
-- Common mistake: This query uses the label. It is an investigation query, not a feature you can compute before the fraud is confirmed.

SELECT customer_id, COUNT(*) AS frauds, SUM(amount) AS fraud_amount
FROM transactions
WHERE is_fraud = 1
GROUP BY customer_id
HAVING COUNT(*) >= 10
ORDER BY frauds DESC, customer_id;
