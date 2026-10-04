-- Loan status counts
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Count loans by status.
--
-- Approach: A one-dimension aggregation is the right first query before any model.
-- Common mistake: Counting customers instead of loans understates exposure when a customer can have one loan in this lab but the grain is the loan.

SELECT status, COUNT(*) AS loans, SUM(principal) AS principal
FROM loans
GROUP BY status
ORDER BY loans DESC;
