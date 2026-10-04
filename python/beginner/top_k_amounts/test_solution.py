from solution import top_k_amounts

def test_top():
    assert top_k_amounts([4, 1, 9, 3], 2) == [9, 4]
    assert top_k_amounts([1], 5) == [1]
