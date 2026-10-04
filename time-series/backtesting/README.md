# Backtesting

Backtesting is not random cross-validation.

## 1. Business problem

Estimate how a rule would have behaved at past decision times, with costs, without using information those times did not have.

## 2. Dataset

Any ordered series in this lab. The index is time. The universe is whoever existed at that time.

## 3. Architecture

`expanding_window_indices` and `rolling_window_indices` in `src/forecasting/backtest.py`. `apply_transaction_cost` charges basis points. Slippage is an extra adverse price you state as an assumption.

## 4. Data pipeline

At origin t, features and the training label horizon end at or before t. A feature batch computed at month end cannot be applied to decisions earlier that month.

## 5. Feature engineering

Same as `time-series/`, rebuilt at each origin. A single feature matrix for the whole sample is how look-ahead sneaks in.

## 6. Baseline

Buy and hold, or the seasonal naive, with the same costs.

## 7. Models

Whatever you would have been allowed to fit at that origin. The model class is less important than the information set.

## 8. Validation

Several origins. Overlapping bets are not independent trials. Do not quote a t-statistic that pretends they are.

## 9. Results

The unit tests check that training indices end before test indices, and that costs reduce the return. They do not certify a strategy.

## 10. Business interpretation

A paper fill at the close is optimistic. State the spread and the capacity. A backtest with unlimited size is a research note.

## 11. Limitations

This laboratory has no order book. Slippage is a parameter, not a measured impact.

## 12. Production considerations

Version the code, the data snapshot, the cost assumption, and the number of trials. Decide the kill criterion before a shadow run.

## 13. Future improvements

A membership table as of each origin, so the universe cannot be chosen at the end of the sample.
