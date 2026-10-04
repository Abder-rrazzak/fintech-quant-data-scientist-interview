-- Fraud rate on monday
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute the fraud rate for monday. In PostgreSQL, EXTRACT(DOW) uses 0 for Sunday.
--
-- Approach: Weekday seasonality is a feature and a monitoring cut. Keep the DOW convention explicit.
-- Common mistake: A quiet Sunday rate can be volume mix, not a safer population.

SELECT COUNT(*) AS transactions,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
WHERE EXTRACT(DOW FROM timestamp) = 1;
