from solution import amount_lookup

def test_lookup():
    assert amount_lookup([1, 1], [5.0, 7.0]) == {1: 7.0}
