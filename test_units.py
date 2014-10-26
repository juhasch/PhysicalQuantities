# -*- coding: utf-8 -*-
import PhysicalQuantities as pq
import numpy as np

def test_unit_division():
    a = pq.Q(1,'m/s')
    assert str(a) == '1 m/s'

def test_scaling():
    k = pq.Q(1e-3, 'km')
    a = pq.Q(1, 'm')
    c = pq.Q(100, 'cm')
    m = pq.Q(1000, 'mm')
    u = pq.Q(1e6, 'um')
    n = pq.Q(1e9, 'nm')
    assert k == a == c == m == u == n

def test_multiplication():
    a = pq.Q(2., 'm')
    b = 1.
    assert a*b == a
    assert b*a == a
    
def test_unit_division():
    a = pq.Q(1, 'mm')
    b = pq.Q(1, 'cm')
    assert type(a/b) == float


def test_unit_multiplication():
    a = pq.Q(1, 'mm')
    b = pq.Q(1, 'cm')
    assert str((a*b).base.unit) == "m^2"

def test_deg():
    a = pq.Q(30, 'deg')
    assert np.sin(a) == np.sin(30/180*pi)
    assert np.cos(a) == np.cos(30/180*pi)

def test_prefix_attributes():
    d = pq.Q(1, 'm')
    assert d.to('mm') ==  d.mm
