from solution import total_from_json

def test_json():
    assert total_from_json('[{"amount": 2}, {"amount": 3.5}]') == 5.5
