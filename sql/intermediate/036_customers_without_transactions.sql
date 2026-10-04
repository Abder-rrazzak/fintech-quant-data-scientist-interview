-- Customers with no transactions
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Return customers who have no rows in transactions.
--
-- Approach: A left join plus IS NULL is the anti-join. NOT EXISTS is the same plan shape on many engines.
-- Common mistake: NOT IN (SELECT customer_id ...) becomes unknown if the subquery can return NULL.

SELECT c.customer_id
FROM customers AS c
LEFT JOIN transactions AS t
  ON c.customer_id = t.customer_id
WHERE t.customer_id IS NULL;
