-- Amounts more than 4 prior standard deviations
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Flag transactions whose amount is more than 4 standard deviations above the customer's history strictly before that transaction.
--
-- Approach: Use a window that ends one row before the current row so the point is not inside its own baseline.
-- Common mistake: Including the current amount in the mean and standard deviation shrinks the z-score of the outlier.

WITH scored AS (
    SELECT transaction_id,
           customer_id,
           amount,
           AVG(amount) OVER (
               PARTITION BY customer_id
               ORDER BY timestamp
               ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
           ) AS prior_mean,
           STDDEV_SAMP(amount) OVER (
               PARTITION BY customer_id
               ORDER BY timestamp
               ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
           ) AS prior_std
    FROM transactions
)
SELECT *
FROM scored
WHERE prior_std > 0
  AND (amount - prior_mean) / prior_std > 4;
