import pandas as pd
from solution import pd_cohort_month

def test_cohort():
    frame = pd.DataFrame({'signup_date': ['2024-01-15', '2024-01-02']})
    assert pd_cohort_month(frame).tolist() == ['2024-01', '2024-01']
