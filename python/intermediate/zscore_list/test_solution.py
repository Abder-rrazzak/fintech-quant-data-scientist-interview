from solution import zscore_list

def test_z():
    assert zscore_list([5.0, 5.0]) == [0.0, 0.0]
