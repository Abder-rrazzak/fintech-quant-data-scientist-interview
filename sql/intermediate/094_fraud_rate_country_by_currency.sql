-- Fraud rate by country and currency
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Break the fraud rate down by country and currency. Include the transaction count.
--
-- Approach: A two-way rate with a HAVING floor is the start of a segment review, not a causal finding.
-- Common mistake: A high rate on a handful of rows is not a reason to block a whole segment.

SELECT country,
       currency,
       COUNT(*) AS transactions,
       SUM(is_fraud) AS frauds,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
GROUP BY 1, 2
HAVING COUNT(*) >= 30
ORDER BY fraud_rate DESC;
