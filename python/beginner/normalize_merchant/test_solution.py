from solution import normalize_merchant

def test_norm():
    assert normalize_merchant('  ACME   Store ') == 'acme store'
