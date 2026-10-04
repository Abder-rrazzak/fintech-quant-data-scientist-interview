from solution import net_return

def test_net():
    assert abs(net_return(0.02, 1.0, 10) - 0.019) < 1e-12
