# -*- coding: utf-8 -*-
import numpy as np

from PhysicalQuantities import isphysicalquantity
from PhysicalQuantities.quantity import PhysicalQuantity


def test_numpy_multiplication():
    a = np.array([1,1])
    b = PhysicalQuantity(1, 'm')
    assert str((a*b)[0].unit) == 'm'
    assert str((b*a)[0].unit) == 'm'    


def test_numpy_division():
    a = np.array([1,1])
    b = PhysicalQuantity(1, 'm')
    assert str((a/b)[0].unit) == '1/m'
    assert str((b/a)[0].unit) == 'm'


def test_indexing():
    a = np.arange(10) * PhysicalQuantity(1, 'm')
    b = a[0:2]
    assert (b.m_ == [0, 1]).all()
