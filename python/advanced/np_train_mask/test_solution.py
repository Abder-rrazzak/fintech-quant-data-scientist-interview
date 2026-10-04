import numpy as np
from solution import np_train_mask

def test_mask():
    stamps = np.array(['2024-01-01', '2024-06-01'], dtype='datetime64[ns]')
    mask = np_train_mask(stamps, np.datetime64('2024-03-01'))
    assert mask.tolist() == [True, False]
