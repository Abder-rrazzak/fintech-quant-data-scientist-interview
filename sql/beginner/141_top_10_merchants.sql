-- Top 10 merchants by spend
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Return the 10 merchants with the highest total amount.
--
-- Approach: Aggregate, order, and limit. Add a tie break so the result is stable.
-- Common mistake: LIMIT without an aggregate returns arbitrary transaction rows, not top merchants.

SELECT merchant_id, SUM(amount) AS spend, COUNT(*) AS transactions
FROM transactions
GROUP BY merchant_id
ORDER BY spend DESC, merchant_id
LIMIT 10;
