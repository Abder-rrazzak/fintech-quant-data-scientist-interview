-- First country seen for the customer
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Attach the customer's earliest transaction country to every later row.
--
-- Approach: FIRST_VALUE needs a frame that can see the first row. The default frame stops at the current row, which happens to include the first row if you are ordered ascending, so the unbounded frame makes the intent obvious.
-- Common mistake: LAST_VALUE with the default frame returns the current row, not the last row in the partition.

SELECT transaction_id,
       customer_id,
       country,
       FIRST_VALUE(country) OVER (
           PARTITION BY customer_id
           ORDER BY timestamp
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS first_country
FROM transactions;
