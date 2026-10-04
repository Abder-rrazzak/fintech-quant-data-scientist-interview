"""Pandas and NumPy exercises."""

from __future__ import annotations

RAW: list[tuple] = []


def A(*row: object) -> None:
    RAW.append(row)


PD = "import pandas as pd"
NP = "import numpy as np"
BOTH = "import numpy as np\nimport pandas as pd"


A("advanced", "pandas", "pd_customer_totals", "Pandas customer totals",
  "Return a Series of amount sums indexed by customer_id.",
  "pd_customer_totals", "frame: pd.DataFrame",
  "return frame.groupby('customer_id', sort=True)['amount'].sum()",
  "import pandas as pd\nfrom solution import pd_customer_totals\n\ndef test_tot():\n    frame = pd.DataFrame({'customer_id': [1, 1, 2], 'amount': [10.0, 5.0, 3.0]})\n    result = pd_customer_totals(frame)\n    assert result.loc[1] == 15.0 and result.loc[2] == 3.0\n",
  PD)
A("advanced", "pandas", "pd_merge_customers", "Merge transactions to customers",
  "Left-join transactions to customers on customer_id.",
  "pd_merge_customers", "transactions: pd.DataFrame, customers: pd.DataFrame",
  "return transactions.merge(customers, on='customer_id', how='left')",
  "import pandas as pd\nfrom solution import pd_merge_customers\n\ndef test_merge():\n    tx = pd.DataFrame({'customer_id': [1], 'amount': [5]})\n    cust = pd.DataFrame({'customer_id': [1], 'country': ['US']})\n    out = pd_merge_customers(tx, cust)\n    assert out.loc[0, 'country'] == 'US'\n",
  PD)
A("advanced", "pandas", "pd_concat_days", "Concatenate daily extracts",
  "Concatenate frames vertically and reset the index.",
  "pd_concat_days", "frames: list[pd.DataFrame]",
  "return pd.concat(frames, ignore_index=True)",
  "import pandas as pd\nfrom solution import pd_concat_days\n\ndef test_concat():\n    a = pd.DataFrame({'amount': [1]})\n    b = pd.DataFrame({'amount': [2]})\n    assert pd_concat_days([a, b])['amount'].tolist() == [1, 2]\n",
  PD)
A("advanced", "pandas", "pd_pivot_month", "Pivot monthly totals",
  "Frame has customer_id, month, amount. Return a customer by month pivot of sums.",
  "pd_pivot_month", "frame: pd.DataFrame",
  "return frame.pivot_table(index='customer_id', columns='month', values='amount', aggfunc='sum', fill_value=0)",
  "import pandas as pd\nfrom solution import pd_pivot_month\n\ndef test_pivot():\n    frame = pd.DataFrame({'customer_id': [1, 1], 'month': ['2024-01', '2024-02'], 'amount': [2.0, 3.0]})\n    out = pd_pivot_month(frame)\n    assert out.loc[1, '2024-01'] == 2.0\n",
  PD)
A("advanced", "pandas", "pd_melt_balances", "Melt wide balances",
  "Melt balance_before and balance_after into a long frame with columns customer_id, field, value.",
  "pd_melt_balances", "frame: pd.DataFrame",
  "return frame.melt(id_vars=['customer_id'], value_vars=['balance_before', 'balance_after'], var_name='field', value_name='value')",
  "import pandas as pd\nfrom solution import pd_melt_balances\n\ndef test_melt():\n    frame = pd.DataFrame({'customer_id': [1], 'balance_before': [5.0], 'balance_after': [4.0]})\n    out = pd_melt_balances(frame)\n    assert set(out['field']) == {'balance_before', 'balance_after'}\n",
  PD)
A("advanced", "pandas", "pd_rolling_mean", "Rolling mean by customer",
  "Frame is sorted by customer_id and timestamp. Return the prior-excluding rolling mean of the last 2 amounts, aligned to the frame.",
  "pd_rolling_mean", "frame: pd.DataFrame",
  "shifted = frame.groupby('customer_id', sort=False)['amount'].shift(1)\nreturn shifted.groupby(frame['customer_id'], sort=False).rolling(2, min_periods=2).mean().reset_index(level=0, drop=True)",
  "import pandas as pd\nfrom solution import pd_rolling_mean\n\ndef test_roll():\n    frame = pd.DataFrame({'customer_id': [1, 1, 1], 'timestamp': [1, 2, 3], 'amount': [10.0, 20.0, 30.0]})\n    out = pd_rolling_mean(frame)\n    assert pd.isna(out.iloc[0]) and pd.isna(out.iloc[1])\n    assert out.iloc[2] == 15.0\n",
  PD)
A("advanced", "pandas", "pd_resample_daily", "Resample to daily totals",
  "timestamp is a datetime column. Return a Series of daily amount sums.",
  "pd_resample_daily", "frame: pd.DataFrame",
  "indexed = frame.set_index('timestamp').sort_index()\nreturn indexed['amount'].resample('D').sum()",
  "import pandas as pd\nfrom solution import pd_resample_daily\n\ndef test_resample():\n    frame = pd.DataFrame({'timestamp': pd.to_datetime(['2024-01-01 01:00', '2024-01-01 05:00', '2024-01-02 01:00']), 'amount': [1.0, 2.0, 4.0]})\n    out = pd_resample_daily(frame)\n    assert out.iloc[0] == 3.0 and out.iloc[1] == 4.0\n",
  PD)
A("advanced", "pandas", "pd_categorical", "Categorical merchant category",
  "Return a copy whose merchant_category is a pandas Categorical with the provided categories.",
  "pd_categorical", "frame: pd.DataFrame, categories: list[str]",
  "out = frame.copy()\nout['merchant_category'] = pd.Categorical(out['merchant_category'], categories=categories)\nreturn out",
  "import pandas as pd\nfrom solution import pd_categorical\n\ndef test_cat():\n    frame = pd.DataFrame({'merchant_category': ['grocery', 'fuel']})\n    out = pd_categorical(frame, ['fuel', 'grocery'])\n    assert str(out['merchant_category'].dtype) == 'category'\n",
  PD)
A("advanced", "pandas", "pd_month_key", "Month key",
  "Return a Series of YYYY-MM strings from a timestamp column.",
  "pd_month_key", "frame: pd.DataFrame",
  "return pd.to_datetime(frame['timestamp']).dt.strftime('%Y-%m')",
  "import pandas as pd\nfrom solution import pd_month_key\n\ndef test_month():\n    frame = pd.DataFrame({'timestamp': ['2024-03-02', '2024-11-01']})\n    assert pd_month_key(frame).tolist() == ['2024-03', '2024-11']\n",
  PD)
A("advanced", "pandas", "pd_vector_zscore", "Vectorized z-score",
  "Return a Series z-score of amount. Do not use apply. Zero std returns zeros.",
  "pd_vector_zscore", "frame: pd.DataFrame",
  "std = frame['amount'].std(ddof=0)\nif std == 0 or pd.isna(std):\n    return frame['amount'] * 0.0\nreturn (frame['amount'] - frame['amount'].mean()) / std",
  "import pandas as pd\nfrom solution import pd_vector_zscore\n\ndef test_z():\n    frame = pd.DataFrame({'amount': [1.0, 2.0, 3.0]})\n    out = pd_vector_zscore(frame)\n    assert abs(out.sum()) < 1e-9\n",
  PD)
A("advanced", "pandas", "pd_chunk_sum", "Sum a CSV in chunks",
  "Sum the amount column of a CSV path using chunksize, so the whole file need not sit in memory.",
  "pd_chunk_sum", "path: str, chunksize: int = 2",
  "total = 0.0\nfor chunk in pd.read_csv(path, chunksize=chunksize, usecols=['amount']):\n    total += float(chunk['amount'].sum())\nreturn total",
  "import os\nimport tempfile\nimport pandas as pd\nfrom solution import pd_chunk_sum\n\ndef test_chunk():\n    handle, name = tempfile.mkstemp(suffix='.csv')\n    os.close(handle)\n    try:\n        with open(name, 'w', encoding='utf-8') as out:\n            out.write('amount\\n1\\n2\\n3\\n')\n        assert pd_chunk_sum(name, chunksize=2) == 6.0\n    finally:\n        os.remove(name)\n",
  PD)
A("advanced", "pandas", "pd_duplicate_ids", "Duplicate transaction ids",
  "Return the sorted list of transaction_id values that occur more than once.",
  "pd_duplicate_ids", "frame: pd.DataFrame",
  "dupes = frame.loc[frame['transaction_id'].duplicated(keep=False), 'transaction_id']\nreturn sorted(dupes.unique().tolist())",
  "import pandas as pd\nfrom solution import pd_duplicate_ids\n\ndef test_dup():\n    frame = pd.DataFrame({'transaction_id': [1, 2, 1]})\n    assert pd_duplicate_ids(frame) == [1]\n",
  PD)
A("advanced", "pandas", "pd_fraud_rate", "Fraud rate by segment",
  "Return a Series of mean is_fraud by customer_segment.",
  "pd_fraud_rate", "frame: pd.DataFrame",
  "return frame.groupby('customer_segment', sort=True)['is_fraud'].mean()",
  "import pandas as pd\nfrom solution import pd_fraud_rate\n\ndef test_rate():\n    frame = pd.DataFrame({'customer_segment': ['a', 'a', 'b'], 'is_fraud': [1, 0, 0]})\n    assert pd_fraud_rate(frame).loc['a'] == 0.5\n",
  PD)
A("advanced", "pandas", "pd_expanding_sum", "Expanding sum by customer",
  "Return the expanding sum of amount within customer_id, including the current row.",
  "pd_expanding_sum", "frame: pd.DataFrame",
  "return frame.groupby('customer_id', sort=False)['amount'].expanding().sum().reset_index(level=0, drop=True)",
  "import pandas as pd\nfrom solution import pd_expanding_sum\n\ndef test_exp():\n    frame = pd.DataFrame({'customer_id': [1, 1], 'amount': [2.0, 5.0]})\n    assert pd_expanding_sum(frame).tolist() == [2.0, 7.0]\n",
  PD)
A("advanced", "pandas", "pd_asof_utilization", "Backward as-of utilization",
  "entities has customer_id and as_of. history has customer_id, event_time, utilization. Both are sorted. Return the backward as-of merge.",
  "pd_asof_utilization", "entities: pd.DataFrame, history: pd.DataFrame",
  "left = entities.sort_values('as_of')\nright = history.sort_values('event_time')\nreturn pd.merge_asof(left, right, left_on='as_of', right_on='event_time', by='customer_id', direction='backward')",
  "import pandas as pd\nfrom solution import pd_asof_utilization\n\ndef test_asof():\n    entities = pd.DataFrame({'customer_id': [1], 'as_of': pd.to_datetime(['2024-03-01'])})\n    history = pd.DataFrame({'customer_id': [1, 1], 'event_time': pd.to_datetime(['2024-01-01', '2024-06-01']), 'utilization': [0.2, 0.9]})\n    out = pd_asof_utilization(entities, history)\n    assert out.loc[0, 'utilization'] == 0.2\n",
  PD)
A("advanced", "numpy", "np_log_returns", "NumPy log returns",
  "Log returns of a positive price array.",
  "np_log_returns", "prices: np.ndarray",
  "prices = np.asarray(prices, dtype=float)\nif np.any(prices <= 0):\n    raise ValueError('price')\nreturn np.diff(np.log(prices))",
  "import numpy as np\nfrom solution import np_log_returns\n\ndef test_ret():\n    out = np_log_returns(np.array([100.0, 110.0]))\n    assert abs(out[0] - np.log(1.1)) < 1e-12\n",
  NP)
A("advanced", "numpy", "np_rolling_sum", "NumPy rolling sum",
  "Sum of each window of length k. Return a shorter array.",
  "np_rolling_sum", "values: np.ndarray, k: int",
  "values = np.asarray(values, dtype=float)\nif k <= 0 or k > len(values):\n    raise ValueError('k')\nwindow = np.ones(k)\nreturn np.convolve(values, window, mode='valid')",
  "import numpy as np\nfrom solution import np_rolling_sum\n\ndef test_roll():\n    assert np_rolling_sum(np.array([1.0, 2.0, 3.0, 4.0]), 2).tolist() == [3.0, 5.0, 7.0]\n",
  NP)
A("advanced", "numpy", "np_zscore", "NumPy z-score",
  "Population z-score. Zero std returns zeros.",
  "np_zscore", "values: np.ndarray",
  "values = np.asarray(values, dtype=float)\nstd = values.std()\nif std == 0:\n    return np.zeros_like(values, dtype=float)\nreturn (values - values.mean()) / std",
  "import numpy as np\nfrom solution import np_zscore\n\ndef test_z():\n    out = np_zscore(np.array([1.0, 2.0, 3.0]))\n    assert abs(out.sum()) < 1e-9\n",
  NP)
A("advanced", "numpy", "np_where_night", "Vectorized night flag",
  "Return 1 for hours 0 through 5, else 0.",
  "np_where_night", "hours: np.ndarray",
  "hours = np.asarray(hours)\nreturn np.where((hours >= 0) & (hours <= 5), 1, 0)",
  "import numpy as np\nfrom solution import np_where_night\n\ndef test_night():\n    assert np_where_night(np.array([1, 12, 5])).tolist() == [1, 0, 1]\n",
  NP)
A("advanced", "numpy", "np_clip_scores", "Clip scores",
  "Clip model scores to [0, 1].",
  "np_clip_scores", "scores: np.ndarray",
  "return np.clip(np.asarray(scores, dtype=float), 0.0, 1.0)",
  "import numpy as np\nfrom solution import np_clip_scores\n\ndef test_clip():\n    assert np_clip_scores(np.array([-0.2, 0.4, 1.3])).tolist() == [0.0, 0.4, 1.0]\n",
  NP)
A("advanced", "numpy", "np_bincount_sum", "Sum amounts by integer customer",
  "customer_ids are non-negative ints. Return the sum of amounts for each id from 0 through max.",
  "np_bincount_sum", "customer_ids: np.ndarray, amounts: np.ndarray",
  "return np.bincount(np.asarray(customer_ids, dtype=int), weights=np.asarray(amounts, dtype=float))",
  "import numpy as np\nfrom solution import np_bincount_sum\n\ndef test_bin():\n    out = np_bincount_sum(np.array([0, 1, 0]), np.array([2.0, 3.0, 4.0]))\n    assert out.tolist() == [6.0, 3.0]\n",
  NP)
A("advanced", "numpy", "np_train_mask", "Boolean time mask",
  "Return a boolean mask for timestamps strictly before the cutoff. timestamps and cutoff are datetime64[ns].",
  "np_train_mask", "timestamps: np.ndarray, cutoff: np.datetime64",
  "return np.asarray(timestamps) < np.datetime64(cutoff, 'ns')",
  "import numpy as np\nfrom solution import np_train_mask\n\ndef test_mask():\n    stamps = np.array(['2024-01-01', '2024-06-01'], dtype='datetime64[ns]')\n    mask = np_train_mask(stamps, np.datetime64('2024-03-01'))\n    assert mask.tolist() == [True, False]\n",
  NP)
A("advanced", "numpy", "np_mae", "Mean absolute error",
  "MAE between two arrays.",
  "np_mae", "y_true: np.ndarray, y_pred: np.ndarray",
  "return float(np.mean(np.abs(np.asarray(y_true, dtype=float) - np.asarray(y_pred, dtype=float))))",
  "import numpy as np\nfrom solution import np_mae\n\ndef test_mae():\n    assert np_mae(np.array([1.0, 2.0]), np.array([1.0, 4.0])) == 1.0\n",
  NP)
A("advanced", "numpy", "np_standardize_columns", "Column standardize",
  "Standardize each column of a 2-D array. A zero-std column becomes zeros.",
  "np_standardize_columns", "features: np.ndarray",
  "x = np.asarray(features, dtype=float)\nstd = x.std(axis=0)\ncentered = x - x.mean(axis=0)\nzero = std == 0\ncentered[:, zero] = 0.0\nsafe = np.where(zero, 1.0, std)\nreturn centered / safe",
  "import numpy as np\nfrom solution import np_standardize_columns\n\ndef test_std():\n    out = np_standardize_columns(np.array([[1.0, 5.0], [3.0, 5.0]]))\n    assert abs(out[:, 0].mean()) < 1e-9\n    assert out[:, 1].tolist() == [0.0, 0.0]\n",
  NP)
A("advanced", "memory", "np_float32_amounts", "Store amounts as float32",
  "Return a float32 copy. This is the memory-reduction step, not a change in business meaning.",
  "np_float32_amounts", "amounts: np.ndarray",
  "return np.asarray(amounts, dtype=np.float32)",
  "import numpy as np\nfrom solution import np_float32_amounts\n\ndef test_f32():\n    out = np_float32_amounts(np.array([1.5, 2.5]))\n    assert out.dtype == np.float32\n    assert out.tolist() == [1.5, 2.5]\n",
  NP)
A("advanced", "pandas", "pd_join_indicator", "Join with indicator",
  "Outer-merge and return the _merge indicator counts as a dict.",
  "pd_join_indicator", "left: pd.DataFrame, right: pd.DataFrame",
  "merged = left.merge(right, on='customer_id', how='outer', indicator=True)\nreturn merged['_merge'].value_counts().to_dict()",
  "import pandas as pd\nfrom solution import pd_join_indicator\n\ndef test_ind():\n    left = pd.DataFrame({'customer_id': [1]})\n    right = pd.DataFrame({'customer_id': [1, 2]})\n    counts = pd_join_indicator(left, right)\n    assert counts['both'] == 1 and counts['right_only'] == 1\n",
  PD)
A("advanced", "pandas", "pd_query_large", "Filter large amounts",
  "Return rows whose amount is strictly greater than the threshold.",
  "pd_query_large", "frame: pd.DataFrame, threshold: float",
  "return frame.loc[frame['amount'] > threshold].reset_index(drop=True)",
  "import pandas as pd\nfrom solution import pd_query_large\n\ndef test_q():\n    frame = pd.DataFrame({'amount': [1.0, 5.0, 9.0]})\n    assert pd_query_large(frame, 4)['amount'].tolist() == [5.0, 9.0]\n",
  PD)
A("advanced", "pandas", "pd_rank_within_month", "Rank within month",
  "Add a column rank_in_month using a dense rank of amount descending within month. The frame is not copied in place; return a copy.",
  "pd_rank_within_month", "frame: pd.DataFrame",
  "out = frame.copy()\nout['rank_in_month'] = out.groupby('month')['amount'].rank(method='dense', ascending=False)\nreturn out",
  "import pandas as pd\nfrom solution import pd_rank_within_month\n\ndef test_rank():\n    frame = pd.DataFrame({'month': ['m', 'm'], 'amount': [5.0, 9.0]})\n    out = pd_rank_within_month(frame)\n    assert out.loc[out['amount'] == 9.0, 'rank_in_month'].iloc[0] == 1\n",
  PD)
A("advanced", "numpy", "np_lag_matrix", "Lag matrix",
  "Row t contains values[t-lags:t] reversed so column 0 is the most recent lag. Target is values[t].",
  "np_lag_matrix", "values: np.ndarray, lags: int",
  "values = np.asarray(values, dtype=float)\nrows = [values[t - lags:t][::-1] for t in range(lags, len(values))]\ntargets = [values[t] for t in range(lags, len(values))]\nreturn np.asarray(rows, dtype=float), np.asarray(targets, dtype=float)",
  "import numpy as np\nfrom solution import np_lag_matrix\n\ndef test_lags():\n    x, y = np_lag_matrix(np.array([1.0, 2.0, 3.0, 4.0]), 2)\n    assert x.shape == (2, 2)\n    assert y.tolist() == [3.0, 4.0]\n    assert x[0].tolist() == [2.0, 1.0]\n",
  NP)
A("advanced", "numpy", "np_sigmoid", "Vectorized sigmoid",
  "Sigmoid of an array with logits clipped to [-30, 30].",
  "np_sigmoid", "logits: np.ndarray",
  "x = np.clip(np.asarray(logits, dtype=float), -30, 30)\nreturn 1.0 / (1.0 + np.exp(-x))",
  "import numpy as np\nfrom solution import np_sigmoid\n\ndef test_sig():\n    assert np_sigmoid(np.array([0.0]))[0] == 0.5\n",
  NP)
A("advanced", "pandas", "pd_memory_bytes", "Estimate frame memory",
  "Return the deep memory usage in bytes.",
  "pd_memory_bytes", "frame: pd.DataFrame",
  "return int(frame.memory_usage(deep=True).sum())",
  "import pandas as pd\nfrom solution import pd_memory_bytes\n\ndef test_mem():\n    frame = pd.DataFrame({'amount': [1.0, 2.0]})\n    assert pd_memory_bytes(frame) > 0\n",
  PD)
A("advanced", "pandas", "pd_fill_category", "Fill missing categories",
  "Fill missing merchant_category with 'unknown' and return a copy.",
  "pd_fill_category", "frame: pd.DataFrame",
  "out = frame.copy()\nout['merchant_category'] = out['merchant_category'].fillna('unknown')\nreturn out",
  "import pandas as pd\nfrom solution import pd_fill_category\n\ndef test_fill():\n    frame = pd.DataFrame({'merchant_category': ['grocery', None]})\n    assert pd_fill_category(frame)['merchant_category'].tolist() == ['grocery', 'unknown']\n",
  PD)
A("advanced", "numpy", "np_confusion", "NumPy confusion counts",
  "Return (tp, fp, tn, fn).",
  "np_confusion", "y_true: np.ndarray, y_pred: np.ndarray",
  "y_true = np.asarray(y_true).astype(int)\ny_pred = np.asarray(y_pred).astype(int)\ntp = int(((y_pred == 1) & (y_true == 1)).sum())\nfp = int(((y_pred == 1) & (y_true == 0)).sum())\ntn = int(((y_pred == 0) & (y_true == 0)).sum())\nfn = int(((y_pred == 0) & (y_true == 1)).sum())\nreturn tp, fp, tn, fn",
  "import numpy as np\nfrom solution import np_confusion\n\ndef test_cm():\n    assert np_confusion(np.array([1, 0, 1, 0]), np.array([1, 1, 0, 0])) == (1, 1, 1, 1)\n",
  NP)
A("advanced", "numpy", "np_cost", "Vectorized business cost",
  "Cost of predicting positive where score >= threshold.",
  "np_cost", "y_true: np.ndarray, scores: np.ndarray, threshold: float, fp_cost: float, fn_cost: float",
  "y_true = np.asarray(y_true).astype(int)\npred = np.asarray(scores, dtype=float) >= threshold\nfp = int((pred & (y_true == 0)).sum())\nfn = int((~pred & (y_true == 1)).sum())\nreturn fp * fp_cost + fn * fn_cost",
  "import numpy as np\nfrom solution import np_cost\n\ndef test_cost():\n    assert np_cost(np.array([1, 0]), np.array([0.2, 0.9]), 0.5, 5, 500) == 505\n",
  NP)
A("advanced", "pandas", "pd_cohort_month", "Signup cohort",
  "Return the YYYY-MM cohort for each signup_date.",
  "pd_cohort_month", "frame: pd.DataFrame",
  "return pd.to_datetime(frame['signup_date']).dt.to_period('M').astype(str)",
  "import pandas as pd\nfrom solution import pd_cohort_month\n\ndef test_cohort():\n    frame = pd.DataFrame({'signup_date': ['2024-01-15', '2024-01-02']})\n    assert pd_cohort_month(frame).tolist() == ['2024-01', '2024-01']\n",
  PD)
A("advanced", "pandas", "pd_lag_amount", "Lag amount within customer",
  "Shift amount by 1 within customer_id.",
  "pd_lag_amount", "frame: pd.DataFrame",
  "return frame.groupby('customer_id', sort=False)['amount'].shift(1)",
  "import pandas as pd\nfrom solution import pd_lag_amount\n\ndef test_lag():\n    frame = pd.DataFrame({'customer_id': [1, 1], 'amount': [4.0, 9.0]})\n    out = pd_lag_amount(frame)\n    assert pd.isna(out.iloc[0]) and out.iloc[1] == 4.0\n",
  PD)
A("advanced", "numpy", "np_expanding_mean", "Expanding mean",
  "Including the current element.",
  "np_expanding_mean", "values: np.ndarray",
  "values = np.asarray(values, dtype=float)\nreturn np.cumsum(values) / np.arange(1, len(values) + 1)",
  "import numpy as np\nfrom solution import np_expanding_mean\n\ndef test_exp():\n    assert np_expanding_mean(np.array([2.0, 4.0, 6.0])).tolist() == [2.0, 3.0, 4.0]\n",
  NP)
A("advanced", "numpy", "np_argmax_amount", "Index of the largest amount",
  "Return the first index of the maximum.",
  "np_argmax_amount", "amounts: np.ndarray",
  "return int(np.argmax(np.asarray(amounts, dtype=float)))",
  "import numpy as np\nfrom solution import np_argmax_amount\n\ndef test_arg():\n    assert np_argmax_amount(np.array([1.0, 4.0, 4.0, 2.0])) == 1\n",
  NP)
A("advanced", "pandas", "pd_between_time", "Rows inside a time window",
  "Include start and exclude end.",
  "pd_between_time", "frame: pd.DataFrame, start: str, end: str",
  "stamps = pd.to_datetime(frame['timestamp'])\nmask = (stamps >= pd.Timestamp(start)) & (stamps < pd.Timestamp(end))\nreturn frame.loc[mask].reset_index(drop=True)",
  "import pandas as pd\nfrom solution import pd_between_time\n\ndef test_between():\n    frame = pd.DataFrame({'timestamp': ['2024-01-01', '2024-06-01'], 'amount': [1, 2]})\n    out = pd_between_time(frame, '2024-01-01', '2024-03-01')\n    assert out['amount'].tolist() == [1]\n",
  PD)
A("advanced", "numpy", "np_rate", "Mean of a binary array",
  "Return the mean as a float. Empty input returns 0.",
  "np_rate", "flags: np.ndarray",
  "flags = np.asarray(flags, dtype=float)\nif len(flags) == 0:\n    return 0.0\nreturn float(flags.mean())",
  "import numpy as np\nfrom solution import np_rate\n\ndef test_rate():\n    assert np_rate(np.array([1, 0, 0, 1])) == 0.5\n    assert np_rate(np.array([])) == 0.0\n",
  NP)
A("advanced", "pandas", "pd_value_counts_norm", "Normalized value counts",
  "Return category shares of merchant_category, sorted by the index.",
  "pd_value_counts_norm", "frame: pd.DataFrame",
  "return frame['merchant_category'].value_counts(normalize=True).sort_index()",
  "import pandas as pd\nfrom solution import pd_value_counts_norm\n\ndef test_vc():\n    frame = pd.DataFrame({'merchant_category': ['a', 'a', 'b', 'b']})\n    out = pd_value_counts_norm(frame)\n    assert out.loc['a'] == 0.5\n",
  PD)
A("advanced", "numpy", "np_pairwise_max", "Elementwise maximum",
  "Elementwise maximum of two equal-length arrays.",
  "np_pairwise_max", "left: np.ndarray, right: np.ndarray",
  "return np.maximum(np.asarray(left, dtype=float), np.asarray(right, dtype=float))",
  "import numpy as np\nfrom solution import np_pairwise_max\n\ndef test_max():\n    assert np_pairwise_max(np.array([1.0, 5.0]), np.array([2.0, 3.0])).tolist() == [2.0, 5.0]\n",
  NP)
A("advanced", "pandas", "pd_dropna_subset", "Drop rows missing keys",
  "Drop rows with null timestamp or amount.",
  "pd_dropna_subset", "frame: pd.DataFrame",
  "return frame.dropna(subset=['timestamp', 'amount']).reset_index(drop=True)",
  "import pandas as pd\nfrom solution import pd_dropna_subset\n\ndef test_drop():\n    frame = pd.DataFrame({'timestamp': ['2024-01-01', None], 'amount': [1.0, 2.0]})\n    assert len(pd_dropna_subset(frame)) == 1\n",
  PD)
A("advanced", "numpy", "np_cumsum_reset", "Cumulative sum",
  "NumPy cumulative sum as a float array.",
  "np_cumsum_reset", "values: np.ndarray",
  "return np.cumsum(np.asarray(values, dtype=float))",
  "import numpy as np\nfrom solution import np_cumsum_reset\n\ndef test_csum():\n    assert np_cumsum_reset(np.array([1.0, 2.0, 3.0])).tolist() == [1.0, 3.0, 6.0]\n",
  NP)
A("advanced", "pandas", "pd_map_segment", "Map a segment code",
  "Map segment through a dictionary. Unknown codes become 'other'.",
  "pd_map_segment", "frame: pd.DataFrame, mapping: dict[str, str]",
  "out = frame.copy()\nout['segment_name'] = out['customer_segment'].map(mapping).fillna('other')\nreturn out",
  "import pandas as pd\nfrom solution import pd_map_segment\n\ndef test_map():\n    frame = pd.DataFrame({'customer_segment': ['a', 'z']})\n    out = pd_map_segment(frame, {'a': 'retail'})\n    assert out['segment_name'].tolist() == ['retail', 'other']\n",
  PD)
A("advanced", "numpy", "np_threshold_flags", "Threshold flags",
  "1 where score >= threshold, else 0, as int.",
  "np_threshold_flags", "scores: np.ndarray, threshold: float",
  "return (np.asarray(scores, dtype=float) >= threshold).astype(int)",
  "import numpy as np\nfrom solution import np_threshold_flags\n\ndef test_flags():\n    assert np_threshold_flags(np.array([0.2, 0.8]), 0.5).tolist() == [0, 1]\n",
  NP)
A("advanced", "pandas", "pd_group_size", "Transactions per customer",
  "Return a Series of row counts by customer_id.",
  "pd_group_size", "frame: pd.DataFrame",
  "return frame.groupby('customer_id', sort=True).size()",
  "import pandas as pd\nfrom solution import pd_group_size\n\ndef test_size():\n    frame = pd.DataFrame({'customer_id': [1, 1, 2]})\n    assert pd_group_size(frame).loc[1] == 2\n",
  PD)
A("advanced", "numpy", "np_safe_divide", "Vectorized safe divide",
  "Divide a by b. Where b is 0, return the fill value.",
  "np_safe_divide", "numerator: np.ndarray, denominator: np.ndarray, fill: float = 0.0",
  "numerator = np.asarray(numerator, dtype=float)\ndenominator = np.asarray(denominator, dtype=float)\nout = np.full(numerator.shape, fill, dtype=float)\nmask = denominator != 0\nout[mask] = numerator[mask] / denominator[mask]\nreturn out",
  "import numpy as np\nfrom solution import np_safe_divide\n\ndef test_div():\n    out = np_safe_divide(np.array([1.0, 1.0]), np.array([2.0, 0.0]), fill=-1)\n    assert out.tolist() == [0.5, -1.0]\n",
  NP)
A("advanced", "pandas", "pd_sort_transactions", "Stable time sort",
  "Sort by customer_id and timestamp with a stable sort.",
  "pd_sort_transactions", "frame: pd.DataFrame",
  "return frame.sort_values(['customer_id', 'timestamp'], kind='mergesort').reset_index(drop=True)",
  "import pandas as pd\nfrom solution import pd_sort_transactions\n\ndef test_sort():\n    frame = pd.DataFrame({'customer_id': [2, 1], 'timestamp': [2, 1], 'amount': [5, 7]})\n    assert pd_sort_transactions(frame)['customer_id'].tolist() == [1, 2]\n",
  PD)
A("advanced", "numpy", "np_unique_counts", "Unique values and counts",
  "Return (values, counts) from np.unique.",
  "np_unique_counts", "values: np.ndarray",
  "return np.unique(np.asarray(values), return_counts=True)",
  "import numpy as np\nfrom solution import np_unique_counts\n\ndef test_unique():\n    values, counts = np_unique_counts(np.array([2, 1, 2]))\n    assert values.tolist() == [1, 2] and counts.tolist() == [1, 2]\n",
  NP)
A("advanced", "pandas", "pd_pct_change", "Percent change within customer",
  "Percent change of amount within customer_id. The first row of each customer is NaN.",
  "pd_pct_change", "frame: pd.DataFrame",
  "return frame.groupby('customer_id', sort=False)['amount'].pct_change()",
  "import pandas as pd\nfrom solution import pd_pct_change\n\ndef test_pct():\n    frame = pd.DataFrame({'customer_id': [1, 1], 'amount': [10.0, 15.0]})\n    out = pd_pct_change(frame)\n    assert pd.isna(out.iloc[0]) and out.iloc[1] == 0.5\n",
  PD)
A("advanced", "numpy", "np_moving_average", "Moving average",
  "Valid-mode moving average of window k.",
  "np_moving_average", "values: np.ndarray, k: int",
  "values = np.asarray(values, dtype=float)\nif k <= 0 or k > len(values):\n    raise ValueError('k')\nkernel = np.ones(k) / k\nreturn np.convolve(values, kernel, mode='valid')",
  "import numpy as np\nfrom solution import np_moving_average\n\ndef test_ma():\n    assert np_moving_average(np.array([1.0, 2.0, 3.0, 4.0]), 2).tolist() == [1.5, 2.5, 3.5]\n",
  NP)
A("advanced", "pandas", "pd_boolean_fraud_rule", "Boolean fraud rule in pandas",
  "Return a boolean Series. Flag when amount_zscore >= 3 or txn_count_1h >= 5.",
  "pd_boolean_fraud_rule", "frame: pd.DataFrame",
  "return (frame['amount_zscore'] >= 3) | (frame['txn_count_1h'] >= 5)",
  "import pandas as pd\nfrom solution import pd_boolean_fraud_rule\n\ndef test_rule():\n    frame = pd.DataFrame({'amount_zscore': [0.2, 3.4], 'txn_count_1h': [1, 1]})\n    assert pd_boolean_fraud_rule(frame).tolist() == [False, True]\n",
  PD)
A("advanced", "numpy", "np_one_hot", "One-hot encode small integers",
  "labels are ints in 0..n_classes-1. Return a float one-hot matrix.",
  "np_one_hot", "labels: np.ndarray, n_classes: int",
  "labels = np.asarray(labels, dtype=int)\nout = np.zeros((len(labels), n_classes), dtype=float)\nout[np.arange(len(labels)), labels] = 1.0\nreturn out",
  "import numpy as np\nfrom solution import np_one_hot\n\ndef test_hot():\n    out = np_one_hot(np.array([0, 2]), 3)\n    assert out.tolist() == [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]\n",
  NP)
A("advanced", "pandas", "pd_sample_weights", "Inverse-frequency weights",
  "Weight each row by 1 / class frequency of is_fraud, so the two classes have equal total weight.",
  "pd_sample_weights", "frame: pd.DataFrame",
  "counts = frame['is_fraud'].value_counts()\nreturn frame['is_fraud'].map(lambda label: 1.0 / counts[label])",
  "import pandas as pd\nfrom solution import pd_sample_weights\n\ndef test_w():\n    frame = pd.DataFrame({'is_fraud': [0, 0, 1]})\n    weights = pd_sample_weights(frame)\n    assert abs(weights[frame['is_fraud'] == 0].sum() - weights[frame['is_fraud'] == 1].sum()) < 1e-9\n",
  PD)
A("advanced", "numpy", "np_rmse", "Root mean squared error",
  "RMSE of two arrays.",
  "np_rmse", "y_true: np.ndarray, y_pred: np.ndarray",
  "err = np.asarray(y_pred, dtype=float) - np.asarray(y_true, dtype=float)\nreturn float(np.sqrt(np.mean(err ** 2)))",
  "import numpy as np\nfrom solution import np_rmse\n\ndef test_rmse():\n    assert abs(np_rmse(np.array([0.0, 0.0]), np.array([3.0, 4.0])) - (12.5 ** 0.5)) < 1e-9\n",
  NP)
A("advanced", "pandas", "pd_cutoff_features", "Drop rows on or after a cutoff",
  "Keep rows with timestamp strictly before the cutoff. This is the point-in-time filter.",
  "pd_cutoff_features", "frame: pd.DataFrame, cutoff: str",
  "stamps = pd.to_datetime(frame['timestamp'])\nreturn frame.loc[stamps < pd.Timestamp(cutoff)].reset_index(drop=True)",
  "import pandas as pd\nfrom solution import pd_cutoff_features\n\ndef test_cut():\n    frame = pd.DataFrame({'timestamp': ['2024-01-01', '2024-08-01'], 'amount': [3.0, 9.0]})\n    out = pd_cutoff_features(frame, '2024-06-01')\n    assert out['amount'].tolist() == [3.0]\n",
  PD)
A("advanced", "numpy", "np_draw_mask", "Reproducible bootstrap indexes",
  "Draw n indexes with replacement from 0..n-1 using a Generator seed.",
  "np_draw_mask", "n: int, seed: int",
  "rng = np.random.default_rng(seed)\nreturn rng.integers(0, n, size=n)",
  "import numpy as np\nfrom solution import np_draw_mask\n\ndef test_draw():\n    first = np_draw_mask(5, 1)\n    second = np_draw_mask(5, 1)\n    assert first.tolist() == second.tolist()\n    assert len(first) == 5\n",
  NP)
A("advanced", "pandas", "pd_nunique_merchants", "Distinct merchants per customer",
  "Return the number of distinct merchant_id values by customer.",
  "pd_nunique_merchants", "frame: pd.DataFrame",
  "return frame.groupby('customer_id', sort=True)['merchant_id'].nunique()",
  "import pandas as pd\nfrom solution import pd_nunique_merchants\n\ndef test_nunique():\n    frame = pd.DataFrame({'customer_id': [1, 1, 1], 'merchant_id': [5, 5, 9]})\n    assert pd_nunique_merchants(frame).loc[1] == 2\n",
  PD)
A("advanced", "pandas", "pd_drop_duplicate_ids", "Drop duplicate ids in pandas",
  "Keep the first row for each transaction_id.",
  "pd_drop_duplicate_ids", "frame: pd.DataFrame",
  "return frame.drop_duplicates('transaction_id', keep='first').reset_index(drop=True)",
  "import pandas as pd\nfrom solution import pd_drop_duplicate_ids\n\ndef test_drop_dup():\n    frame = pd.DataFrame({'transaction_id': [1, 1, 2], 'amount': [3, 8, 1]})\n    assert pd_drop_duplicate_ids(frame)['amount'].tolist() == [3, 1]\n",
  PD)
A("advanced", "numpy", "np_corr", "Pearson correlation",
  "Return the Pearson correlation of two equal-length arrays. Raise ValueError if either array has zero variance.",
  "np_corr", "left: np.ndarray, right: np.ndarray",
  "left = np.asarray(left, dtype=float)\nright = np.asarray(right, dtype=float)\nif left.std() == 0 or right.std() == 0:\n    raise ValueError('variance')\nreturn float(np.corrcoef(left, right)[0, 1])",
  "import numpy as np\nfrom solution import np_corr\n\ndef test_corr():\n    assert abs(np_corr(np.array([1.0, 2.0, 3.0]), np.array([2.0, 4.0, 6.0])) - 1) < 1e-9\n",
  NP)
A("advanced", "numpy", "np_hour_sin", "Cyclic hour encoding",
  "Encode an hour 0-23 as sin(2 pi hour / 24). This lets a model see that 23 and 0 are close.",
  "np_hour_sin", "hours: np.ndarray",
  "hours = np.asarray(hours, dtype=float)\nreturn np.sin(2 * np.pi * hours / 24.0)",
  "import numpy as np\nfrom solution import np_hour_sin\n\ndef test_hour():\n    assert abs(np_hour_sin(np.array([0.0]))[0]) < 1e-9\n    assert abs(np_hour_sin(np.array([6.0]))[0] - 1) < 1e-9\n",
  NP)
A("advanced", "pandas", "pd_clip_amount", "Clip the amount column",
  "Return a copy with amount clipped to [low, high].",
  "pd_clip_amount", "frame: pd.DataFrame, low: float, high: float",
  "out = frame.copy()\nout['amount'] = out['amount'].clip(low, high)\nreturn out",
  "import pandas as pd\nfrom solution import pd_clip_amount\n\ndef test_clip():\n    frame = pd.DataFrame({'amount': [-1.0, 5.0, 20.0]})\n    assert pd_clip_amount(frame, 0, 10)['amount'].tolist() == [0.0, 5.0, 10.0]\n",
  PD)
A("advanced", "numpy", "np_log1p_clip", "Vectorized log1p",
  "Clip negatives to zero, then log1p.",
  "np_log1p_clip", "amounts: np.ndarray",
  "return np.log1p(np.clip(np.asarray(amounts, dtype=float), 0, None))",
  "import numpy as np\nfrom solution import np_log1p_clip\n\ndef test_log():\n    out = np_log1p_clip(np.array([0.0, -4.0]))\n    assert out.tolist() == [0.0, 0.0]\n",
  NP)

