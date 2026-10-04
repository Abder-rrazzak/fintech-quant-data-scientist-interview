from solution import customer_totals

def test_totals():
    assert customer_totals([(1, 10.0), (1, 2.5), (2, 4.0)]) == {1: 12.5, 2: 4.0}
