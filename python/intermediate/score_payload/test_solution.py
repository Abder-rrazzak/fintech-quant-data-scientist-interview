from solution import score_payload

def test_payload():
    assert score_payload({'b': 1, 'a': 2}) == '{"a": 2, "b": 1}'
