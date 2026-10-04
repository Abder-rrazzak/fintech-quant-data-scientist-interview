-- Customers with credit score below 620
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Count customers and their average income with credit_score below 620.
--
-- Approach: A score cut is a policy. Report the count under the cut, not only the average score.
-- Common mistake: The same cut on a different scorecard is not the same risk.

SELECT COUNT(*) AS customers,
       AVG(income) AS avg_income,
       AVG(credit_score) AS avg_score
FROM customers
WHERE credit_score < 620;
