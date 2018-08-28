from numpy.testing import assert_almost_equal

from PhysicalQuantities import PhysicalQuantity, q
import PhysicalQuantities.currency


def test_euro():
    a = PhysicalQuantity(1, 'Euro')
    assert_almost_equal(a.value, 1)


def test_floordiv():
    a = PhysicalQuantity(8, 'Euro')
    b = PhysicalQuantity(2, 'Euro')
    assert a//b == 4

