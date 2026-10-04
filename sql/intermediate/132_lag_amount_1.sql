-- Amount lagged by 1 transactions
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- For each transaction, show the customer's amount 1 transactions earlier.
--
-- Approach: LAG(amount, 1) stays inside the customer partition and cannot see the future.
-- Common mistake: A lag of rows is not a lag of days. Say which one the feature definition uses.

SELECT transaction_id,
       customer_id,
       amount,
       LAG(amount, 1) OVER (PARTITION BY customer_id ORDER BY timestamp) AS lagged_amount
FROM transactions;
