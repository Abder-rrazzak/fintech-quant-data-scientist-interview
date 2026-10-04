-- Previous amount
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Show each transaction and the previous amount for that customer.
--
-- Approach: LAG is the previous row in the specified order. It is a legitimate feature if that row is already known.
-- Common mistake: LAG is not the previous calendar day when the customer skipped a day.

SELECT transaction_id,
       customer_id,
       amount,
       LAG(amount) OVER (PARTITION BY customer_id ORDER BY timestamp) AS previous_amount
FROM transactions;
