# Statistics interview

One hundred or more statistics questions live in `mock-interviews/question_bank.json` under topic `statistics`. Each item has:

1. Intuition — `answer_30s`
2. The explanation you can defend — `answer_2min` and `deep_dive`
3. A Python hook — `statistics/worked_examples.py` for the fraud-rate comparison, and `src/evaluation/inference.py` for intervals, the two-proportion z-test, and the bootstrap
4. The interview prompt — `prompt`
5. The model answer — `answer_2min`
6. The common trap — `common_mistake`

## Fraud rate example

A move from 0.15% to 0.35% is a business event only after you know the counts. `fraud_rate_change` returns a difference, a z-statistic, a p-value, and two normal intervals. A small p-value with a tiny base is still a small number of cases. A large difference with a tiny sample is often noise. Say both.

## Concepts the bank covers

Probability, conditional probability, Bayes, distributions, expectation, variance, covariance, correlation, sampling, the central limit theorem, confidence intervals, hypothesis tests, p-values, type I and type II errors, power, effect size, bootstrap, permutation tests, A/B tests, multiple comparisons, and Bayesian updates at a conceptual level.
