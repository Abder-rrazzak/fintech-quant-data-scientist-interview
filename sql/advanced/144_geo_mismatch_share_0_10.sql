-- Customers with country mismatch share above 0.10
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- A mismatch is a transaction country different from the customer's home country. Return customers whose mismatch share exceeds 0.10 and who have at least 5 transactions.
--
-- Approach: Define the mismatch with a join to the home country, then threshold the share and the sample size together.
-- Common mistake: A single foreign transaction on a new customer is not the same evidence as a 50% mismatch rate on a long history.

SELECT t.customer_id,
       AVG((t.country <> c.country)::int) AS mismatch_share,
       COUNT(*) AS transactions
FROM transactions AS t
JOIN customers AS c
  ON t.customer_id = c.customer_id
GROUP BY t.customer_id
HAVING COUNT(*) >= 5
   AND AVG((t.country <> c.country)::int) > 0.10;
