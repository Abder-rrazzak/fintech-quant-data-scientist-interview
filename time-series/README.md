# Time series

Do not randomly split a financial series.

## 1. Business problem

Forecast a later period using only information available at the origin, and know when the forecast is worse than a seasonal naive.

## 2. Dataset

`market_data` from the generator (a geometric random walk on business days) and aggregated transaction spend. The teaching calendar is train 2020–2023, validate 2024, test 2025.

## 3. Architecture

`src/forecasting/series.py` for returns, log returns, ACF, Durbin-Levinson PACF, and an OLS AR(1). `src/forecasting/backtest.py` for origins.

## 4. Data pipeline

Aggregate to the decision frequency first. A missing day is not a zero unless the business says inactivity is zero.

## 5. Feature engineering

Lags strictly before the target time, rolling mean, rolling volatility, and calendar terms. Sine and cosine of hour or month avoid a jump at the boundary. A scaler is fit inside each training origin.

## 6. Baseline

Seasonal naive: the last matching season. A fancier model has to beat it on a later season.

## 7. Models

AR(1) is implemented. SARIMA and exponential smoothing are the interview extensions: fit them only inside an origin, with statsmodels if you add it. Gradient boosting on lags is reasonable when the walk-forward error beats the naive. A PyTorch LSTM is optional and has to clear the same bar.

## 8. Validation

Expanding or rolling origins. `assert_causal_splits` refuses a window whose training index reaches the test index.

## 9. Results

Report error in the unit finance plans in, on 2024 and then once on 2025. Do not tune on 2025.

## 10. Business interpretation

A small RMSE on standardized data is not a planning number. Translate it.

## 11. Limitations

The market series is a simulated random walk with drift. It will not teach you a tradable edge. Survivorship is avoided here because the universe is synthetic and fixed; say that, and say you would build membership as of each origin on real names.

## 12. Production considerations

Retrain when walk-forward error jumps and stays high, or when the input distribution moves. One bad day is not a structural break.

## 13. Future improvements

A quantile forecast scored with pinball loss, so the interval is tested and not only the point.
