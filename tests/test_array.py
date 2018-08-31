"""Test PhysicalQuantityArray"""

import numpy as np
from PhysicalQuantities import QA
from PhysicalQuantities.unit import UnitError
from numpy.testing import assert_almost_equal
from pytest import raises


def test_unit():
    a = np.random.randn(10)
    b = QA(a, 'm')
    assert str(b.unit) == 'm'


def test_ufunc():
    a = np.random.randn(10)
    b = QA(a, 'm')
    assert_almost_equal((b+b).view(np.ndarray), a+a)


def test_to():
    a = np.random.randn(10)
    b = QA(a, 'mm')
    c = b.to('m')
    assert_almost_equal((c+c).view(np.ndarray)*1e3, a+a)


def test_to_multiple():
    a = np.random.randn(10)
    b = QA(a, 'm/s')
    with raises(ValueError):
        b.to('km/h', 'km/s')


def test_ufunc_fail():
    a = np.random.randn(10)
    b = QA(a, 'm')
    c = QA(a, 's')
    with raises(ValueError):
        b+c


def test_dir():
    a = np.random.randn(10)
    b = QA(a, 'm')
    assert len(b.__dir__()) > 10


def test_getattr():
    a = np.random.randn(10)
    b = QA(a, 'm')
    c = b.m
    assert_almost_equal(b, c)


def test_getattr_dropunit():
    a = np.random.randn(10)
    b = QA(a, 'm')
    c = b.m_
    assert_almost_equal(b, c)


def test_base():
    a = np.random.randn(10)
    b = QA(a, 'm')
    c = b.base
    assert_almost_equal(b, c)


def test_base_2():
    a = np.random.randn(10)
    b = QA(a, 'm/s')
    c = b.base
    assert_almost_equal(b, c)


def test_repr():
    a = np.random.randn(10)
    b = QA(a, 'm')
    assert len(b.__repr__()) > 5


def test_add_same_units():
    a = np.random.randn(10)
    b = QA(a, 'm')
    c = b+b
    assert_almost_equal((b+b).view(np.ndarray), a+a)
    assert c.unit == b.unit


def test_add_different_units():
    a = np.random.randn(10)
    b = QA(a, 'm')
    c = QA(a, 's')
    with raises(UnitError):
        b+c


def test_subtract_same_units():
    a = QA(np.random.randn(10), 'm')
    b = QA(np.random.randn(10), 'm')
    assert_almost_equal((a-b).view(np.ndarray), a+b)
    assert a.unit == b.unit


def test_subtract_different_units():
    a = QA(np.random.randn(10), 'm')
    b = QA(np.random.randn(10), 's')
    with raises(UnitError):
        a-b


def test_multiply_different_units():
    a = QA(np.random.randn(10), 'm')
    b = QA(np.random.randn(10), 's')
    c = a*b
    assert str(c.unit) == 'm*s'
    assert_almost_equal(c, a.view(np.ndarray)*b.view(np.ndarray))


def test_square():
    a = QA(np.random.randn(10), 'm')
    b = a**2
    assert_almost_equal(b, a.view(np.ndarray)**2)
    assert str(b.unit) == 'm^2'


def test_power():
    a = QA(np.random.randn(10), 'm')
    b = a**3
    assert_almost_equal(b, a.view(np.ndarray)**3)
    assert str(b.unit) == 'm^3'
