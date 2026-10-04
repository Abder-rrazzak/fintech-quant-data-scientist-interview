-- Loans with a 30-day delinquency
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Find loans that have at least one payment with days_past_due >= 30.
--
-- Approach: Aggregate to the loan and filter with HAVING, because the condition is on a group.
-- Common mistake: WHERE days_past_due >= 30 before the group still works here, but HAVING is the right tool for an aggregate predicate.

SELECT loan_id,
       customer_id,
       MAX(days_past_due) AS worst_dpd
FROM payments
GROUP BY loan_id, customer_id
HAVING MAX(days_past_due) >= 30;
