-- Next amount for the customer
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Show each transaction and the customer's next amount. The last transaction has a null lead.
--
-- Approach: LEAD looks forward. It is useful in analysis and dangerous as a training feature.
-- Common mistake: Using LEAD as a model feature is look-ahead leakage.

SELECT transaction_id,
       customer_id,
       amount,
       LEAD(amount) OVER (PARTITION BY customer_id ORDER BY timestamp) AS next_amount
FROM transactions;
