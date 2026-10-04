-- Spend buckets with NTILE(4)
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Split customers into 4 buckets by total spend.
--
-- Approach: NTILE assigns buckets after the customer grain is built. Do not ntile raw transactions if the decision is about customers.
-- Common mistake: Bucket edges from a small sample will not match next month. Refit or use fixed cut points for a policy.

WITH totals AS (
    SELECT customer_id, SUM(amount) AS total_amount
    FROM transactions
    GROUP BY customer_id
)
SELECT customer_id,
       total_amount,
       NTILE(4) OVER (ORDER BY total_amount) AS spend_bucket
FROM totals;
