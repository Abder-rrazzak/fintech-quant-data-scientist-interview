-- Spend quintiles
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Assign customers to five quintiles by total amount, 1 being the lowest.
--
-- Approach: NTILE splits the ordered customers into buckets. Uneven counts go to the earlier buckets.
-- Common mistake: Quintiles on a short book are unstable. Do not treat the cut points as a permanent policy.

WITH totals AS (
    SELECT customer_id, SUM(amount) AS total_amount
    FROM transactions
    GROUP BY customer_id
)
SELECT customer_id,
       total_amount,
       NTILE(5) OVER (ORDER BY total_amount) AS spend_quintile
FROM totals;
