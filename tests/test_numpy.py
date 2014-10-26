# -*- coding: utf-8 -*-
import PhysicalQuantities as pq
import numpy as np

def test_numpy_multiplication():
    a = np.array([1,1])
    b = pq.Q(1,'m')
    assert str((a*b)[0].unit) == 'm'
    assert str((b*a)[0].unit) == 'm'    
    
def test_numpy_division():
    a = np.array([1,1])
    b = pq.Q(1,'m')
    assert str((a/b)[0].unit) == '1/m'
    assert str((b/a)[0].unit) == 'm'
