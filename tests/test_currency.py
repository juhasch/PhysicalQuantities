from numpy.testing import assert_almost_equal
from PhysicalQuantities import PhysicalQuantity
import PhysicalQuantities.currency


def test_euro():
    a = PhysicalQuantity(1, 'EUR')
    assert_almost_equal(a.value, 1)


def test_floordiv():
    a = PhysicalQuantity(8, 'EUR')
    b = PhysicalQuantity(2, 'EUR')
    assert a//b == 4


def test_usd():
    """Test might fail if exchange rate cannot be retrieved"""
    a = PhysicalQuantity(1, 'USD')
    assert_almost_equal(a.value, 1)


def test_usd():
    """Test might fail if exchange rate cannot be retrieved"""
    a = PhysicalQuantity(1, 'GBP')
    assert_almost_equal(a.value, 1)


def test_convert():
    """Test might fail if exchange rate cannot be retrieved"""
    a = PhysicalQuantity(1, 'EUR')
    b = PhysicalQuantity(1, 'USD')
    assert a != b.EUR

