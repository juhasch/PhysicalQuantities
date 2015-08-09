# -*- coding: utf-8 -*-
from PhysicalQuantities.dBQuantity import dBQuantity, dB, dB10, dB20
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


def test_comparison_dB():
    g1 = dBQuantity(0,'dB')
    g2 = dBQuantity(1,'dB')
    g3 = dBQuantity(-1,'dB')
    assert g1 > g3
    assert g1 < g2
    assert g1 == g1
    assert g1 >= g3
    assert g1 <= g2


def test_comparison_dBm():
    g1 = dBQuantity(0,'dBm')
    g2 = dBQuantity(1,'dBm')
    g3 = dBQuantity(-1,'dBm')
    assert g1 > g3
    assert g1 < g2
    assert g1 == g1
    assert g1 >= g3
    assert g1 <= g2


def test_calculation():
    g = dBQuantity(0,'dBm')
    a = dBQuantity(10,'dB')
    ga = dBQuantity(10,'dBm')
    assert a + g == ga
    assert g + a == ga


def test_dB():
    assert dB10(10) ==  dBQuantity(10,'dB')
    assert dB20(10) ==  dBQuantity(20,'dB')
    a = PhysicalQuantity(10, 'V')
    b = dBQuantity(20,'dBV')
    c = dB(a)
    assert b == c


def test_numpy_dB():
    a = np.array([1, 2, 3])
    b = a * PhysicalQuantity(1, 'V')
    c = dB(b)
    assert_almost_equal(c.lin.value, a)
