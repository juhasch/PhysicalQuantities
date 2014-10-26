# -*- coding: utf-8 -*-
import PhysicalQuantities as pq

def test_decorators():
    """ Test .base and .value decorators """
    g=pq.Q(98, 'mm')/ pq.Q(1, 's**2')
    assert g.value == 98
    assert g.base.value == 0.098
    assert str(g.unit) == "mm/s^2"    
    
def test_autoscale():
    """ Unit autoscaling """
    a = pq.Q(1e-3, 'm')
    b = a.autoscale()
    assert str(a.mm) == str(b)
    a = pq.Q(1e3, 'm')
    b = a.autoscale()
    assert str(a.km) == str(b)

def test_comparison():
    a = pq.Q(1e-3, 'm')
    b = pq.Q(1, 'mm')
    assert a == b
    
def test_less_than():
    a = pq.Q(1, 'm')
    b = pq.Q(2, 'm')
    assert a < b
    
def test_larger_than():
    a = pq.Q(2, 'm')
    b = pq.Q(3, 'm')
    assert a < b
