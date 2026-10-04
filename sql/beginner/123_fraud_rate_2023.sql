-- Fraud rate in 2023
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute transaction count, fraud count, and fraud rate for calendar year 2023.
--
-- Approach: Use a half-open timestamp range rather than a function on the column.
-- Common mistake: EXTRACT(YEAR FROM timestamp) = {year} is correct and often prevents a plain index seek.

SELECT COUNT(*) AS transactions,
       SUM(is_fraud) AS frauds,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
WHERE timestamp >= TIMESTAMP '2023-01-01'
  AND timestamp < TIMESTAMP '2024-01-01';
