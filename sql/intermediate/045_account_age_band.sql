-- Transactions on young accounts
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Return transactions where account_age_days is under 30, with the customer segment.
--
-- Approach: The age on the transaction is a snapshot. Joining the customer table adds attributes that were not denormalized.
-- Common mistake: Filtering on a current account-open date at scoring time is a different feature from the age stored on the historical row.

SELECT t.transaction_id, t.customer_id, t.amount, t.account_age_days, c.customer_segment
FROM transactions AS t
JOIN customers AS c
  ON t.customer_id = c.customer_id
WHERE t.account_age_days < 30;
