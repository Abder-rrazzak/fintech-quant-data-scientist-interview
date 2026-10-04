from solution import first_index_above

def test_idx():
    assert first_index_above([1, 4, 9], 5) == 2
    assert first_index_above([1, 2], 5) == -1
