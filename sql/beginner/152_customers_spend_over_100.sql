-- Customers with spend over 100
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Return customers whose total transaction amount exceeds 100.
--
-- Approach: HAVING filters after the aggregate. WHERE cannot see SUM.
-- Common mistake: Putting SUM(amount) > {spend} in WHERE is a syntax error.

SELECT customer_id, SUM(amount) AS spend, COUNT(*) AS transactions
FROM transactions
GROUP BY customer_id
HAVING SUM(amount) > 100
ORDER BY spend DESC;
