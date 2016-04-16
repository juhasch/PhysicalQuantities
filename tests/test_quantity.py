# -*- coding: utf-8 -*-
from PhysicalQuantities.Quantity import PhysicalQuantity
from PhysicalQuantities import isphysicalquantity, q
from PhysicalQuantities.Unit import UnitError
from numpy.testing import assert_almost_equal
import numpy as np
from nose.tools import raises
import operator


def test_str():
    a = PhysicalQuantity(1,'m/s')
    assert str(a) == '1 m/s'


def test_scaling():
    k = PhysicalQuantity(1e-3, 'km')
    a = PhysicalQuantity(1, 'm')
    c = PhysicalQuantity(100, 'cm')
    m = PhysicalQuantity(1000, 'mm')
    u = PhysicalQuantity(1e6, 'um')
    n = PhysicalQuantity(1e9, 'nm')
    assert k == a == c == m == u == n


def test_prefix_attributes():
    d = PhysicalQuantity(1, 'm')
    assert d.to('mm') ==  d.mm


def test_isphysicalquantity():
    g = PhysicalQuantity(1, 'mm')
    assert isphysicalquantity(g) is True
    assert isphysicalquantity(1) is False


def test_rint():
    g = PhysicalQuantity(1.1, 'mm')
    assert g.rint() == PhysicalQuantity(1, 'mm')
    

def test_dir():
    g = PhysicalQuantity(1, 'mm')
    l = g.__dir__()
    assert 'value' in l
    assert 'unit' in l
    assert 'mm' in l


def test_getattr():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(1e-3, 'm')
    assert a.mm == a
    assert a.m == b
    assert a.mm_ == 1
    assert_almost_equal(a.m_, b.m_)
    assert_almost_equal(a.m_, 1e-3)


def test_getattr2():
    a = PhysicalQuantity(3, 'mm')
    assert a._ == 3


def test_decorators():
    """ Test .base and .value decorators """
    g = PhysicalQuantity(98, 'mm')/ PhysicalQuantity(1, 's**2')
    assert g.value == 98
    assert g.base.value == 0.098
    assert str(g.unit) == "mm/s^2"    


def test_getitem():
    a = [1, 2, 3] * PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(1, 'mm')
    assert a[0] == b


def test_setitem():
    a = [1, 2, 3] * PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(5, 'mm')
    a[0] = b
    assert a[0] == b


def test_len():
    a = [1, 2, 3] * PhysicalQuantity(1, 'mm')
    assert len(a) == 3


def test_str():
    b = PhysicalQuantity(5, 'mm')
    assert str(b) == '5 mm'


def test_complex():
    b = PhysicalQuantity(2 + 1j, 'mm')
    assert_almost_equal(complex(b), 0.002+0.001j)


def test_float():
    b = PhysicalQuantity(5, 'mm')
    assert_almost_equal(float(b), 5e-3)


def test_repr_markdown():
    b = PhysicalQuantity(1, 'mm')
    assert b._repr_markdown_() == '1 $\\text{mm}$'


def test_sum():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(2, 'mm')
    assert a+b == PhysicalQuantity(3, 'mm')


def test_sub():
    a = PhysicalQuantity(3, 'mm')
    b = PhysicalQuantity(1, 'mm')
    assert a-b == PhysicalQuantity(2, 'mm')


def test_mul():
    a = PhysicalQuantity(2, 'mm')
    b = PhysicalQuantity(3, 'mm')
    assert a*b == PhysicalQuantity(6, 'mm**2')


def test_mul_1():
    a = PhysicalQuantity(2, 'mm')
    b = PhysicalQuantity(3, '1/mm')
    assert a*b == 6


def test_div():
    a = PhysicalQuantity(3, 'mm**2')
    b = PhysicalQuantity(4, 'mm')
    assert a/b == PhysicalQuantity(3/4, 'mm')
    assert b/b == 1


def test_eq():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(2, 'm')
    assert a == a
    assert not a == b


def test_eq_prefixed():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(2, 'mm')
    assert a == a
    assert not a == b


def test_ne():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(2, 'm')
    assert a != b
    assert not a != a


def test_ne_prefixed():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(2, 'mm')
    assert a != b
    assert not a != a


def test_lt():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(2, 'm')
    assert a < b
    assert not a < a


def test_lt_prefixed():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(2, 'mm')
    assert a < b
    assert not a < a


def test_le():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(2, 'm')
    assert a <= b
    assert a <= a


def test_le_prefixed():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(2, 'mm')
    assert a <= b
    assert a <= a


def test_gt():
    a = PhysicalQuantity(2, 'm')
    b = PhysicalQuantity(1, 'm')
    assert a > b
    assert not a > a


def test_gt_prefixed():
    a = PhysicalQuantity(2, 'mm')
    b = PhysicalQuantity(1, 'mm')
    assert a > b
    assert not a > a


def test_ge():
    a = PhysicalQuantity(2, 'm')
    b = PhysicalQuantity(1, 'm')
    assert a >= b
    assert a >= a


def test_ge_prefixed():
    a = PhysicalQuantity(2, 'mm')
    b = PhysicalQuantity(1, 'mm')
    assert a >= b
    assert a >= a


def test_to():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1000, 'mm')
    assert a.to('mm') == b


def test_to_1():
    a = PhysicalQuantity(4000, 'mm/s')
    assert a.to('m/s') == a


def test_base():
    a = PhysicalQuantity(1, 'V')
    b = PhysicalQuantity(1, 'kg*m^2/A/s^3')
    assert a.base == b


def test_real():
    b = PhysicalQuantity(2 + 1j, 'V')
    assert b.real == PhysicalQuantity(2, 'V')


def test_imag():
    b = PhysicalQuantity(2 + 1j, 'V')
    assert b.imag == PhysicalQuantity(1, 'V')


def test_pow_builtin():
    a = PhysicalQuantity(2, 'm')
    b = PhysicalQuantity(4, 'm**2')
    assert a.pow(2) == b
    assert a**2 == b


def test_pow_builtin_prefixed():
    a = PhysicalQuantity(4, 'mm')
    b = PhysicalQuantity(16, 'mm**2')
    assert pow(a, 2) == b


def test_sqrt():
    a = PhysicalQuantity(2, 'mm')
    b = PhysicalQuantity(4, 'mm**2')
    assert b.pow(0.5) == a
    assert b**0.5 == a


def test_sqrt2():
    a = PhysicalQuantity(2, 'mm')
    b = PhysicalQuantity(4, 'mm**2')
    assert b.sqrt() == a


def test_autoscale():
    """ Unit autoscaling """
    a = PhysicalQuantity(1e-3, 'm')
    b = a.autoscale
    assert str(a.mm) == str(b)
    a = PhysicalQuantity(1e3, 'm')
    b = a.autoscale
    assert str(a.km) == str(b)


def test_format():
    a = PhysicalQuantity(1.123123, 'm')
    assert str(a) == '1.123123 m'
    a.format = '.3f'
    assert str(a) == '1.123 m'


def test_round():
    a = PhysicalQuantity(1.123123, 'm')
    b = round(a)
    assert b.value == 1


def test_round_2():
    a = np.array([1.2, 2.8]) * PhysicalQuantity(1, 'm')
    b = round(a)
    assert_almost_equal(b.value, np.array([1, 3]))


def test_floordiv():
    a = PhysicalQuantity(4, 'm')
    b = PhysicalQuantity(2, 'm')
    c = a // b
    assert c == 2


def test_floordiv_1():
    a = PhysicalQuantity(4, 'm')
    b = 2
    c = a // b
    assert c.value == 2


def test_rfloordiv():
    a = 4
    b = PhysicalQuantity(2, 'm')
    c = a // b
    assert c.value == 2


@raises(UnitError)
def test_rpow():
    a = PhysicalQuantity(4, 'm')
    b = 2
    b**a


def test_pos():
    a = PhysicalQuantity(4, 'm')
    assert operator.pos(a) == a
  
  
def test_pos_np():
    a = np.array([1, 2]) * PhysicalQuantity(1, 'm')
    assert np.any(operator.pos(a) == a)

    
def test_neg():
    a = PhysicalQuantity(4, 'm')
    assert operator.neg(a) == -a


def test_neg_np():
    a = np.array([1, 2]) * PhysicalQuantity(1, 'm')
    assert np.any(operator.neg(a) == -a)


def test_nonzero():
    assert PhysicalQuantity(4, 'm').__nonzero__() == True
    assert PhysicalQuantity(0, 'm').__nonzero__() == False


def test_nonzero_np():
    r = (np.array([3, 0, 1]) * PhysicalQuantity(1, 'm')).__nonzero__()
    assert np.any(r.value == np.array([0, 2]))


def test_is_angle():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'deg')
    c = PhysicalQuantity(1, 'rad')
    assert a.unit.is_angle is False
    assert b.unit.is_angle is True
    assert c.unit.is_angle is True


def test_markdown():
    a = PhysicalQuantity(1, 'm')
    assert a.unit.markdown == '$\\text{m}$'


def test_name():
    a = PhysicalQuantity(1, 'm')
    assert a.unit.name == 'm'


def test_deg():
    a = PhysicalQuantity(30, 'deg')
    assert np.sin(a) == np.sin(30/180*np.pi)
    assert np.cos(a) == np.cos(30/180*np.pi)


def test_sin():
    a = PhysicalQuantity(0, 'deg')
    assert a.sin() == 0


def test_cos():
    a = PhysicalQuantity(0, 'deg')
    assert a.cos() == 1

    
def test_tan():
    a = PhysicalQuantity(0, 'deg')
    assert a.tan() == 0


def test_q_1():
    """Test for iitems"""
    a = q['m']
    assert a == PhysicalQuantity(1, 'm')


@raises(KeyError)
def test_q_2():
    """Test for invalid units"""
    a = q['xxm']


def test_q_3():
    """Test for attributes"""
    a = q.m
    assert a == PhysicalQuantity(1, 'm')


def test_ipython_key_completions_():
    l = q._ipython_key_completions_()
    assert len(l) > 1
