import pandas as pd
from solution import pd_asof_utilization

def test_asof():
    entities = pd.DataFrame({'customer_id': [1], 'as_of': pd.to_datetime(['2024-03-01'])})
    history = pd.DataFrame({'customer_id': [1, 1], 'event_time': pd.to_datetime(['2024-01-01', '2024-06-01']), 'utilization': [0.2, 0.9]})
    out = pd_asof_utilization(entities, history)
    assert out.loc[0, 'utilization'] == 0.2
