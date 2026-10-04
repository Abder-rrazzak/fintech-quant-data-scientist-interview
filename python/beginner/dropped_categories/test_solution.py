from solution import dropped_categories

def test_dropped():
    assert dropped_categories(['atm', 'fuel'], ['fuel']) == ['atm']
