-- luxury versus grocery
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compare fraud rate and average ticket for merchant_category 'luxury' against grocery.
--
-- Approach: Hold the comparison set to two categories so the reader sees a baseline, not a sorted list of everything.
-- Common mistake: A higher fraud rate at a category can be mix, ticket size, or channel. Do not jump to a block rule from one query.

SELECT merchant_category,
       COUNT(*) AS transactions,
       AVG(amount) AS avg_ticket,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
WHERE merchant_category IN ('luxury', 'grocery')
GROUP BY merchant_category;
