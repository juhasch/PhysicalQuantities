# -*- coding: utf-8 -*-
from PhysicalQuantities.dBQuantity import dBQuantity, dB10, dB20
from PhysicalQuantities import PhysicalQuantity
from numpy.testing import assert_almost_equal
import numpy as np

def test_basic_properties():
    g = dBQuantity(0.1,'dBm')
    assert g.value == 0.1
    assert g.unit == 'dBm'
    assert g.factor == 10
    assert_almost_equal(g.lin.value, 1.023292992280754)


def test_conversion():
    g = dBQuantity(0,'dBm')
    glin = PhysicalQuantity(1, 'mW')
    assert g.mW == glin
    assert g.mW_ == 1
    assert g.dBW_ == -30
    assert g.W_ == 0.001


def test_gt_dB():
    g1 = dBQuantity(0,'dB')
    g2 = dBQuantity(1,'dB')
    g3 = dBQuantity(-1,'dB')
    assert g1 > g3
    assert g2 > g3
    assert not g3 > g1


def test_lt_dB():
    g1 = dBQuantity(0,'dB')
    g2 = dBQuantity(1,'dB')
    g3 = dBQuantity(-1,'dB')
    assert g1 < g2
    assert g3 < g2
    assert not g1 > g2


def test_eq_dB():
    g1 = dBQuantity(0,'dB')
    g2 = dBQuantity(1,'dB')
    assert g1 == g1
    assert not g1 == g2


def test_ne_db():
    g1 = dBQuantity(0,'dB')
    g2 = dBQuantity(1,'dB')
    assert g1 != g2
    assert not g1 != g1


def test_ge_dB():
    g1 = dBQuantity(0,'dB')
    g2 = dBQuantity(1,'dB')
    g3 = dBQuantity(-1,'dB')
    assert g2 >= g1
    assert g1 >= g1
    assert not g3 >= g1


def test_le_dB():
    g1 = dBQuantity(0,'dB')
    g2 = dBQuantity(1,'dB')
    g3 = dBQuantity(-1,'dB')
    assert g3 <= g3
    assert g3 <= g1
    assert not g2 <= g1


def test_calculation():
    g = dBQuantity(0,'dBm')
    a = dBQuantity(10,'dB')
    ga = dBQuantity(10,'dBm')
    assert a + g == ga
    assert g + a == ga


def test_numpy_dB():
    a = np.array([1, 2, 3])
    b = a * PhysicalQuantity(1, 'V')
    c = b.dB
    assert_almost_equal(c.lin, a)


def test_numpy_to_dB():
    a = np.array([1, 2, 3])
    b = a * PhysicalQuantity(1, 'V')
    c = b.to_dB()
    assert_almost_equal(c.lin.value, a)

def test_add_dB():
    g1 = dBQuantity(1,'dB')
    g2 = dBQuantity(2,'dB')
    assert (g1 + g2).value == 3


def test_sub_dB():
    g1 = dBQuantity(1,'dB')
    g2 = dBQuantity(2,'dB')
    assert (g1 - g2).value == -1


def test_dB10():
    a = dB10(100)
    b = dB10(0.1)
    assert a.value == 20
    assert b.value == -10


def test_dB20():
    a = dB20(100)
    b = dB20(0.1)
    assert a.value == 40
    assert b.value == -20


def test_dB_1():
    a = PhysicalQuantity(10, 'V')
    b = a.to_dB()
    assert b == dBQuantity(20, 'dBV')


def test_dB_2():
    a = PhysicalQuantity(10, 'nV')
    b = a.to_dB()
    assert b == dBQuantity(20, 'dBnV')


def setitem():
    a = np.ones(2) * dBQuantity(1, 'dBm')
    a[0] = dBQuantity(2, 'dBm')
    assert a[0] == dBQuantity(2, 'dBm')
