""" Test imperial units """
from numpy.testing import assert_almost_equal

from PhysicalQuantities import PhysicalQuantity
import PhysicalQuantities.imperial


def test_inch():
    a = PhysicalQuantity(1, 'inch')
    assert_almost_equal(a.mm_, 25.4)


def test_ft():
    a = PhysicalQuantity(1, 'ft')
    assert_almost_equal(a.mm_, 304.8)


def test_yd():
    a = PhysicalQuantity(1, 'yd')
    assert_almost_equal(a.mm_, 914.4)


def test_mi():
    a = PhysicalQuantity(1, 'mi')
    assert_almost_equal(a.m_, 1609.344)


def test_nmi():
    a = PhysicalQuantity(1, 'nmi')
    assert_almost_equal(a.m_, 1852.0)


def test_furlong():
    a = PhysicalQuantity(1, 'furlong')
    assert_almost_equal(a.m_, 201.168)


def test_acres():
    a = PhysicalQuantity(1, 'acres')
    assert(a.base.unit.name == 'm**2')
    assert_almost_equal(a.to('m**2').value, 4046.8564224)


def test_b():
    """ Barn """
    a = PhysicalQuantity(1, 'barn')
    assert(a.base.unit.name == 'm')
    assert_almost_equal(a.base.value, 1e-28)


def test_tsp():
    """ Teaspoon """
    a = PhysicalQuantity(1, 'tsp')
    assert(a.base.unit.name == 'm**3')
    assert_almost_equal(a.base.value, 4.928921593750001e-06)


def test_floz():
    """ Fluid ounce """
    a = PhysicalQuantity(1, 'floz')
    assert(a.base.unit.name == 'm**3')
    assert_almost_equal(a.base.value, 2.9573529562500008e-05)


def test_cup():
    a = PhysicalQuantity(1, 'cup')
    b = PhysicalQuantity(1, 'floz')
    assert(a.base.unit.name == 'm**3')
    assert(a == 8*b)


def test_pint():
    a = PhysicalQuantity(1, 'pt')
    b = PhysicalQuantity(1, 'floz')
    assert(a.base.unit.name == 'm**3')
    assert(a == 16*b)


def test_qt():
    a = PhysicalQuantity(1, 'qt')
    b = PhysicalQuantity(1, 'pt')
    assert(a.base.unit.name == 'm**3')
    assert(a == 2*b)


def test_galUS():
    a = PhysicalQuantity(1, 'galUS')
    b = PhysicalQuantity(1, 'qt')
    assert(a.base.unit.name == 'm**3')
    assert(a == 4*b)


def test_galUK():
    a = PhysicalQuantity(1, 'galUK')
    b = PhysicalQuantity(4546.09, 'cm**3')
    assert(a.base.unit.name == 'm**3')
    assert(a == b)


def test_oz():
    a = PhysicalQuantity(1, 'oz')
    assert(a.base.unit.name == 'kg')
    assert_almost_equal(a.base.value, 0.028349523125)


def test_lb():
    a = PhysicalQuantity(1, 'lb')
    b = PhysicalQuantity(16, 'oz')
    assert(a.base.unit.name == 'kg')
    assert(a == b)


def test_ton():
    a = PhysicalQuantity(1, 'ton')
    b = PhysicalQuantity(2000, 'lb')
    assert(a.base.unit.name == 'kg')
    assert(a == b)


def test_Btu():
    a = PhysicalQuantity(1, 'Btu')
    b = PhysicalQuantity(1055.05585262, 'J')
    assert(a == b)


def test_hp():
    a = PhysicalQuantity(1, 'hp')
    b = PhysicalQuantity(745.7, 'W')
    assert(a == b)


def test_psi():
    a = PhysicalQuantity(1, 'psi')
    b = PhysicalQuantity(6894.75729317, 'Pa')


def test_degF():
    a = PhysicalQuantity(0, 'degF')
    assert_almost_equal(a.K_, 255.37222222222223)
    a = PhysicalQuantity(100, 'degF')
    assert_almost_equal(a.K_,310.9277777777778)


def test_degF2():
    a = PhysicalQuantity(0, 'degF')
    assert(a.base.value == 255.37222222222223)
