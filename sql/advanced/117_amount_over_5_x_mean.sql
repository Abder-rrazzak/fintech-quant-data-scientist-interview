-- Amount over 5 times the customer mean
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Find transactions whose amount exceeds 5 times that customer's average amount. Then explain why the average in this query is slightly biased.
--
-- Approach: Join the customer mean and filter. Say that this mean includes the current row, so a production feature should use prior rows only.
-- Common mistake: Shipping the inclusive mean as a live feature makes extreme amounts look closer to normal than they were at decision time.

WITH stats AS (
    SELECT customer_id, AVG(amount) AS avg_amount
    FROM transactions
    GROUP BY customer_id
)
SELECT t.transaction_id, t.customer_id, t.amount, s.avg_amount
FROM transactions AS t
JOIN stats AS s
  ON t.customer_id = s.customer_id
WHERE s.avg_amount > 0
  AND t.amount > s.avg_amount * 5;
