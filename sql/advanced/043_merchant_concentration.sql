-- Share of spend in the top merchant
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- For each customer, compute the share of amount that went to their single largest merchant.
--
-- Approach: Aggregate to the merchant, rank inside the customer, and divide by the customer total.
-- Common mistake: The customer total must be computed before filtering to rank 1, or the share becomes 1 by construction.

WITH by_merchant AS (
    SELECT customer_id,
           merchant_id,
           SUM(amount) AS merchant_amount,
           SUM(SUM(amount)) OVER (PARTITION BY customer_id) AS customer_amount
    FROM transactions
    GROUP BY customer_id, merchant_id
), ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY customer_id
               ORDER BY merchant_amount DESC, merchant_id
           ) AS rn
    FROM by_merchant
)
SELECT customer_id,
       merchant_id,
       merchant_amount / NULLIF(customer_amount, 0) AS top_merchant_share
FROM ranked
WHERE rn = 1;
