from pytest import raises
from PhysicalQuantities import q


def test_m():
    """Check if extended prefixes get added to q.m"""
    assert q.m == q.m
    with raises(KeyError):
        assert q.Ym == q.Ym
    import PhysicalQuantities.extend_prefixed
    assert q.Ym == q.Ym
