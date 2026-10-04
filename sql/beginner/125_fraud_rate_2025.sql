-- Fraud rate in 2025
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute transaction count, fraud count, and fraud rate for calendar year 2025.
--
-- Approach: Use a half-open timestamp range rather than a function on the column.
-- Common mistake: EXTRACT(YEAR FROM timestamp) = {year} is correct and often prevents a plain index seek.

SELECT COUNT(*) AS transactions,
       SUM(is_fraud) AS frauds,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
WHERE timestamp >= TIMESTAMP '2025-01-01'
  AND timestamp < TIMESTAMP '2026-01-01';
