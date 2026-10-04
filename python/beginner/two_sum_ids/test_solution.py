from solution import two_sum_ids

def test_two_sum():
    assert two_sum_ids([2.0, 7.0, 11.0, 15.0], 18.0) == [1, 2]
    assert two_sum_ids([1.0, 2.0], 10.0) is None
