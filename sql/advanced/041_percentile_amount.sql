-- Amount percentile by segment
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Within each customer_segment, return the 95th percentile of transaction amount using a window percentile.
--
-- Approach: PERCENTILE_CONT is the continuous percentile. PERCENTILE_DISC returns an observed value.
-- Common mistake: A global percentile hides that affluent and mass-market tickets are different populations.

SELECT DISTINCT customer_segment,
       PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY amount) AS p95_amount
FROM transactions
GROUP BY customer_segment;
