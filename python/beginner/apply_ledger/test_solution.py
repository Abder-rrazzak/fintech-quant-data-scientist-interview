from solution import apply_ledger

def test_ledger():
    assert apply_ledger(100, [('withdraw', 40), ('deposit', 10)]) == 70
    try:
        apply_ledger(5, [('withdraw', 6)])
        raise AssertionError('expected')
    except ValueError:
        pass
