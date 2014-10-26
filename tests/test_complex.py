# -*- coding: utf-8 -*-
import PhysicalQuantities as pq

def test_complex_assign():
    """ wrap complex number with quantity """
    a = (1+2j) * pq.Q(1,'V')
    assert str(a) == '(1+2j) V'
    
def test_complex_attr():
    """ test getting real/imaginary part 
        real/imag attributes of complex numbers always return floats...
    """
    a = (1.0+2.0j) * pq.Q(1,'V')
    assert str(a.real) == '1.0 V'
    assert str(a.imag) == '2.0 V'

def test_complex_mag():
    """ Test magnitude computation """
    a = (1+2j) * pq.Q(1,'V')
    b = abs(a)
    TOL = 1e-15
    assert abs((b - (a.real**2 +a.imag**2)**0.5).value) < TOL
