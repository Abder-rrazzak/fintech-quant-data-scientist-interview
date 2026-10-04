-- Payment shortfall
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- For each loan, sum amount_due minus amount_paid.
--
-- Approach: Shortfall is an amount, not a rate. Report both if the audience might confuse them.
-- Common mistake: A customer can look current on a rate and still owe a large dollar shortfall.

SELECT loan_id,
       customer_id,
       SUM(amount_due - amount_paid) AS shortfall
FROM payments
GROUP BY loan_id, customer_id
HAVING SUM(amount_due - amount_paid) > 0
ORDER BY shortfall DESC;
