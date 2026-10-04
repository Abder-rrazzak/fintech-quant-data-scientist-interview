-- Monthly retention by signup cohort
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- For each signup month, compute how many customers transacted in each later month, and the retention rate versus the cohort size.
--
-- Approach: Attach a cohort date that does not change, then count distinct active customers by later month.
-- Common mistake: Defining the cohort from the first transaction drops customers who never transact and answers a different question.

WITH cohort AS (
    SELECT customer_id,
           date_trunc('month', signup_date)::date AS cohort_month
    FROM customers
), activity AS (
    SELECT DISTINCT customer_id,
           date_trunc('month', timestamp)::date AS active_month
    FROM transactions
)
SELECT c.cohort_month,
       a.active_month,
       COUNT(*) AS active_customers,
       COUNT(*)::numeric / NULLIF(COUNT(*) OVER (PARTITION BY c.cohort_month), 0) AS retention
FROM cohort AS c
JOIN activity AS a
  ON c.customer_id = a.customer_id
 AND a.active_month >= c.cohort_month
GROUP BY c.cohort_month, a.active_month;
