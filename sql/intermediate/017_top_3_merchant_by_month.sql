-- Top 3 merchants by monthly amount
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- For each calendar month, return the top 3 merchants by total amount. Break ties by merchant_id.
--
-- Approach: Aggregate, then ROW_NUMBER partitioned by month. Filter rn <= 3.
-- Common mistake: RANK keeps ties and can return more than k rows. Say which behavior you want.

WITH monthly AS (
    SELECT date_trunc('month', timestamp)::date AS month_start,
           merchant_id AS entity_id,
           SUM(amount) AS total_amount
    FROM transactions
    GROUP BY 1, 2
), ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY month_start
               ORDER BY total_amount DESC, entity_id
           ) AS rn
    FROM monthly
)
SELECT month_start, entity_id, total_amount, rn
FROM ranked
WHERE rn <= 3;
