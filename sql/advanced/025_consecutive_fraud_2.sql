-- 2 consecutive fraudulent transactions
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Find customers with at least 2 consecutive transactions flagged is_fraud = 1, ordered by time.
--
-- Approach: Gaps-and-islands: the difference of two row numbers is constant inside a consecutive run.
-- Common mistake: Counting frauds in a day is not the same as consecutive transactions.

WITH ordered AS (
    SELECT customer_id,
           timestamp,
           is_fraud,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY timestamp) AS rn,
           ROW_NUMBER() OVER (PARTITION BY customer_id, is_fraud ORDER BY timestamp) AS rn_flag
    FROM transactions
), islands AS (
    SELECT customer_id,
           rn - rn_flag AS island_key,
           COUNT(*) AS run_length
    FROM ordered
    WHERE is_fraud = 1
    GROUP BY customer_id, rn - rn_flag
)
SELECT customer_id, run_length
FROM islands
WHERE run_length >= 2;
