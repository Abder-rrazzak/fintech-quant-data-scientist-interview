-- Trailing 30 days amount
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- For each transaction, compute the sum of that customer's amounts over the trailing 30 days, including the current transaction. The frame must not see future rows.
--
-- Approach: A window ordered by time, with RANGE limited to the trailing interval, is the point-in-time sum.
-- Common mistake: ROWS BETWEEN 7 PRECEDING is seven rows, not seven days.

SELECT transaction_id,
       customer_id,
       timestamp,
       amount,
       SUM(amount) OVER (
           PARTITION BY customer_id
           ORDER BY timestamp
           RANGE BETWEEN INTERVAL '30 days' PRECEDING AND CURRENT ROW
       ) AS trailing_amount
FROM transactions;
