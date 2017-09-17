# -*- coding: utf-8 -*-
import numpy as np

import PhysicalQuantities as pq


def test_list_0():
    """ wrap quantity around list """
    a = [1,2,3] * pq.Q(1,'m')
    assert str(a) == '[1, 2, 3] m'


def test_list_1():
    """ access list via index """
    a = [1,2,3] * pq.Q(1,'m')
    assert str(a[0]) == '1 m'


def test_list_2(): # BUG!
    """ assign list via index """
    a = [1.0, 2.0, 3.0] * pq.Q(1,'m')
    a[1] = a[2]
    assert str(a[1]) == '3.0 m'


def test_list_3():
    """ index range """
    a = [1,2,3] * pq.Q(1,'m')
    assert str(a[0:2]) == '[1, 2] m'


def test_array_0():
    """ wrap quantity around numpy array """
    a = np.array([1,2,3]) * pq.Q(1,'m')
    assert str(a) == '[1 2 3] m'


def test_array_1():
    """ access list via index """
    a = np.array([1,2,3]) * pq.Q(1,'m')
    assert str(a[0]) == '1 m'


def test_array_2(): # BUG!
    """ assign list via index """
    a = np.array([1,2,3]) * pq.Q(1,'m')
    a[1] = a[2]
    assert str(a[1]) == '3 m'


def test_array_3():
    """ index range """
    a = np.array([1,2,3]) * pq.Q(1,'m')
    assert str(a[0:2]) == '[1 2] m'
