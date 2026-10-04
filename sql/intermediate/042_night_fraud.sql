-- Fraud rate by night versus day
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Treat hours 0 through 5 as night. Compare fraud rate and volume.
--
-- Approach: Put the hour rule in a CASE so the two rates are one aggregation, not two queries that can drift.
-- Common mistake: A higher night rate with tiny volume may not be a stable segment.

SELECT CASE WHEN EXTRACT(HOUR FROM timestamp) BETWEEN 0 AND 5 THEN 'night' ELSE 'day' END AS day_part,
       COUNT(*) AS transactions,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
GROUP BY 1;
