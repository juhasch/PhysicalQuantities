# -*- coding: utf-8 -*-
from PhysicalQuantities.Quantity import PhysicalQuantity, UnitError
import PhysicalQuantities.numpywrapper as nw
from numpy.testing import assert_almost_equal
import numpy as np
from nose.tools import raises


def test_max():
    a = np.array([1.3, 2.5]) * PhysicalQuantity(1, 'mm')
    assert_almost_equal(nw.max(a).value, 2.5)


def test_floor():
    a = np.array([1.3, 2.5]) * PhysicalQuantity(1, 'mm')
    assert_almost_equal(nw.floor(a).value, np.array([1, 2]))


def test_ceil_1():
    a = np.array([1.3, 2.5]) * PhysicalQuantity(1, 'mm')
    assert_almost_equal(nw.ceil(a).value, np.array([2, 3]))


def test_ceil_2():
    a = np.array([1.3, 2.5])
    assert_almost_equal(nw.ceil(a), np.array([2, 3]))


def test_sqrt_1():
    a = np.array([4, 9]) * PhysicalQuantity(1, 'm^2')
    assert_almost_equal(nw.sqrt(a).value, np.array([2, 3]))
    assert nw.sqrt(a).unit == PhysicalQuantity(1, 'm').unit


def test_sqrt_2():
    a = np.array([4, 9])
    assert_almost_equal(nw.sqrt(a), np.array([2, 3]))


def test_linspace_1():
    a = nw.linspace(PhysicalQuantity(1, 'mm'), PhysicalQuantity(10, 'mm'), 10)
    b = np.linspace(1, 10, 10)
    assert_almost_equal(a.value, b)


def test_linspace_2():
    a = nw.linspace(1, 10, 10)
    b = np.linspace(1, 10, 10)
    assert_almost_equal(a, b)


@raises(UnitError)
def test_linspace_3():
    a = nw.linspace(PhysicalQuantity(1, 'mm'), PhysicalQuantity(10, 's'), 10)
    assert(a)


def test_linspace_4():
    a = nw.linspace(PhysicalQuantity(1, 'mm'), 10, 10)
    b = np.linspace(1, 10, 10)
    assert_almost_equal(a.value, b)


def test_linspace_5():
    a, b = nw.linspace(PhysicalQuantity(1, 'mm'), PhysicalQuantity(10, 'mm'), 10, retstep=True)
    c, d = nw.linspace(1, 10, 10, retstep=True)
    assert_almost_equal(a.value, c)
    assert(b.value == d)


def test_linspace_6():
    a = nw.linspace(1, PhysicalQuantity(10, 'mm'), 10)
    b = np.linspace(1, 10, 10)
    assert_almost_equal(a.value, b)


def test_tophysicalquantity_1():
    # conversion of PQ array elements to PQ array
    a = [ PhysicalQuantity(1, 'mm'), PhysicalQuantity(2, 'm'), PhysicalQuantity(3, 'mm')]
    b = nw.tophysicalquantity(a)
    assert_almost_equal(b.value, np.array([1, 2000, 3]))


@raises(UnitError)
def test_tophysicalquantity_2():
    # single value
    a = 1
    b = nw.tophysicalquantity(a)
    assert a == b

    
def test_tophysicalquantity_3():
    # single value
    a = 1
    b = nw.tophysicalquantity(a, 'Hz')
    assert a == b.value


def test_tophysicalquantity_4():
    # single value
    a = PhysicalQuantity(2, 'Hz')
    b = nw.tophysicalquantity(a)
    assert a == b


def test_tophysicalquantity_5():
    # already an array
    a = [ 1, 2, 3] * PhysicalQuantity(1, 'mm')
    b = nw.tophysicalquantity(a)
    assert_almost_equal(a.value, b.value)
    assert a.unit == b.unit


def test_argsort_1():
    x = np.array([3, 1, 2])
    y = np.argsort(x)
    _x = x * PhysicalQuantity(1, 'm^2')
    _y = nw.argsort(_x)
    assert_almost_equal( _y, y)


def test_argsort_2():
    x = np.array([3, 1, 2])
    y = np.argsort(x)
    z = nw.argsort(x)
    assert_almost_equal( y, z)


def test_insert_1():
    x = np.array([1, 2, 3]) * PhysicalQuantity(1, 'm')
    y = nw.insert( x, 0, PhysicalQuantity(4, 'm'))
    assert_almost_equal( y.value, np.array([4, 1, 2, 3]))
    

def test_insert_2():
    x = np.array([1, 2, 3])
    y = np.insert(x, 0, 4)
    z = nw.insert(x, 0, 4)
    assert_almost_equal( y, z)
