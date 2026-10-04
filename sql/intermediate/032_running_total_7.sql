-- Running amount by customer, 7-day hint
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute a running total of amount per customer in timestamp order. In the interview, say how you would restrict it to 7 days if the business asked.
--
-- Approach: A running total is SUM with the default expanding frame. A trailing window replaces UNBOUNDED PRECEDING.
-- Common mistake: Ordering only by timestamp without partitioning mixes customers together.

SELECT transaction_id,
       customer_id,
       timestamp,
       amount,
       SUM(amount) OVER (
           PARTITION BY customer_id
           ORDER BY timestamp
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_amount
FROM transactions;
