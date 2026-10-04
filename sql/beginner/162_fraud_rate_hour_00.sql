-- Fraud rate during hour 0
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute the fraud rate and transaction count for timestamp hour 0.
--
-- Approach: A single-hour slice is a diagnostic. Compare it with the book rate before calling it a pattern.
-- Common mistake: Hour is timezone-dependent. Say which clock the timestamp uses.

SELECT COUNT(*) AS transactions,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
WHERE EXTRACT(HOUR FROM timestamp) = 0;
