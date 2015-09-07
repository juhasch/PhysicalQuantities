# -*- coding: utf-8 -*-
from PhysicalQuantities.Quantity import PhysicalQuantity
import PhysicalQuantities.numpywrapper as nw
from numpy.testing import assert_almost_equal
import numpy as np


def test_floor():
    a = np.array([1.3, 2.5]) * PhysicalQuantity(1, 'mm')
    assert_almost_equal(nw.floor(a).value, np.array([1, 2]))


def test_ceil():
    a = np.array([1.3, 2.5]) * PhysicalQuantity(1, 'mm')
    assert_almost_equal(nw.ceil(a).value, np.array([2, 3]))


def test_sqrt():
    a = np.array([4, 9]) * PhysicalQuantity(1, 'm^2')
    assert_almost_equal(nw.sqrt(a).value, np.array([2, 3]))


def test_linspace():
    a = nw.linspace(PhysicalQuantity(1, 'mm'), PhysicalQuantity(10, 'mm'), 10)
    b = np.linspace(1, 10, 10)
    assert_almost_equal(a.value, b)


