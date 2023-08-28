from pytest import raises
from PhysicalQuantities import q


def test_extend_prefixes():
    """Check if extended prefixes get added to q.m"""
    assert q.m == q.m
    assert q.sr == q.sr
    assert q.Hz == q.Hz

    with raises(KeyError):
        assert q.Ym == q.Ym

    with raises(KeyError):
        assert q.Ysr == q.Ysr

    with raises(KeyError):        
        assert q.YHz == q.YHz
    
    import PhysicalQuantities.extend_prefixed
    assert q.Ym == q.Ym
    assert q.Ysr == q.Ysr
    assert q.YHz == q.YHz
