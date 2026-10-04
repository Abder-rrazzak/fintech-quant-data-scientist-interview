from solution import all_customers

def test_union():
    assert all_customers([1, 2], [2, 3]) == [1, 2, 3]
