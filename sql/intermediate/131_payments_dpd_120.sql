-- Payments at least 120 days past due
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Count payments and customers with days_past_due >= 120.
--
-- Approach: A delinquency bucket is a policy definition. State the DPD cut before quoting the rate.
-- Common mistake: Customers and payments are different grains. A customer rate and a payment rate answer different questions.

SELECT COUNT(*) AS payments,
       COUNT(DISTINCT customer_id) AS customers,
       SUM(amount_due - amount_paid) AS shortfall
FROM payments
WHERE days_past_due >= 120;
