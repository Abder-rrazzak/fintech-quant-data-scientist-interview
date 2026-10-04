from solution import merge_amount_dicts

def test_merge():
    assert merge_amount_dicts({'a': 1.0}, {'a': 2.0, 'b': 3.0}) == {'a': 3.0, 'b': 3.0}
