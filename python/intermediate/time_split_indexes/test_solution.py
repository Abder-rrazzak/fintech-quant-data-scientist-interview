from solution import time_split_indexes

def test_idx():
    train_end, valid_end = time_split_indexes(100)
    assert 0 < train_end < valid_end < 100
