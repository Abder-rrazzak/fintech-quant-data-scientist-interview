from solution import decision_message

def test_msg():
    assert decision_message('review', 0.2) == 'decision=review score=0.200'
