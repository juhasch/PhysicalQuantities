"""Test PhysicalQuantityArray"""

import numpy as np
from PhysicalQuantities import QA
from numpy.testing import assert_almost_equal


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
