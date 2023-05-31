import pytest
from numpy.testing import assert_almost_equal
from PhysicalQuantities import PhysicalQuantity
from PhysicalQuantities.currency import CurrencyRates


def test_euro():
    a = PhysicalQuantity(1, 'EUR')
    assert_almost_equal(a.value, 1)


def test_floordiv():
    a = PhysicalQuantity(8, 'EUR')
    b = PhysicalQuantity(2, 'EUR')
    assert a//b == 4


@pytest.mark.skipif(CurrencyRates() is None, reason="requires forex_python")
def test_usd():
    """Test might fail if exchange rate cannot be retrieved"""
    a = PhysicalQuantity(1, 'USD')
    assert_almost_equal(a.value, 1)


@pytest.mark.skipif(CurrencyRates() is None, reason="requires forex_python")
def test_gbp():
    """Test might fail if exchange rate cannot be retrieved"""
    a = PhysicalQuantity(1, 'GBP')
    assert_almost_equal(a.value, 1)


@pytest.mark.skipif(CurrencyRates() is None, reason="requires forex_python")
def test_convert():
    """Test might fail if exchange rate cannot be retrieved"""
    a = PhysicalQuantity(1, 'EUR')
    b = PhysicalQuantity(1, 'USD')
    assert a != b.EUR

