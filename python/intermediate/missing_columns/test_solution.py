from solution import missing_columns

def test_missing():
    assert missing_columns(['amount'], ['amount', 'country']) == ['country']
