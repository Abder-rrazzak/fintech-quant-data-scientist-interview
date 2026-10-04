-- Fraud rate by country and month
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute the fraud rate and the fraud count by transaction country and calendar month.
--
-- Approach: Fraud rate is the mean of a 0/1 flag. Always return the denominator next to the rate.
-- Common mistake: Averaging a rate of rates, weighted equally by country, is not the portfolio fraud rate.

SELECT country,
       date_trunc('month', timestamp)::date AS month_start,
       COUNT(*) AS transactions,
       SUM(is_fraud) AS frauds,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
GROUP BY 1, 2
ORDER BY 2, 1;
