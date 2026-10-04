-- Portfolio expected loss
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- For each defaulted-or-not loan, compute PD stand-in default_12m times lgd times ead, then the book sum. This is a teaching query, not a capital model.
--
-- Approach: Expected loss adds facility-level PD x LGD x EAD. Here the realized 0/1 label stands in for PD only as a classroom query.
-- Common mistake: Do not use the realized default flag as a feature in the model that is supposed to predict it.

SELECT SUM(default_12m * lgd * ead) AS portfolio_expected_loss,
       AVG(default_12m::numeric) AS observed_default_rate
FROM loans;
