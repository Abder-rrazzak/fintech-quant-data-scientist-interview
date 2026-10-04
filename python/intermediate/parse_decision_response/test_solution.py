from solution import parse_decision_response

def test_response():
    assert parse_decision_response('{"decision": "review"}') == 'review'
