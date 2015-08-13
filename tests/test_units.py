# -*- coding: utf-8 -*-
from PhysicalQuantities import PhysicalQuantity
from PhysicalQuantities.Unit import isphysicalunit
import numpy as np


def test_unit_division():
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


def test_multiplication():
    a = PhysicalQuantity(2., 'm')
    b = 1.
    assert a*b == a
    assert b*a == a


def test_unit_division_2():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(1, 'cm')
    assert type(a/b) == float


def test_unit_multiplication():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(1, 'cm')
    assert str((a*b).base.unit) == "m^2"


def test_deg():
    a = PhysicalQuantity(30, 'deg')
    assert np.sin(a) == np.sin(30/180*np.pi)
    assert np.cos(a) == np.cos(30/180*np.pi)


def test_prefix_attributes():
    d = PhysicalQuantity(1, 'm')
    assert d.to('mm') ==  d.mm


def test_unit_inversion():
    a = PhysicalQuantity(1, 'm')
    b = 1/a
    assert np.any(np.array(b.unit.powers) -np.array(a.unit.powers) == 0)


def test_aggregation():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 's')
    c = a*b
    p = [a.unit.powers[i] + b.unit.powers[i] for i in range(len(a.unit.powers))]
    assert p == c.unit.powers


def test_eq():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'mm')
    assert a.unit == a.unit


def test_ne():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'mm')
    assert a.unit != b.unit

def test_lt():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'mm')
    assert b.unit < a.unit
    assert not a.unit < a.unit


def test_le():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'mm')
    assert b.unit <= a.unit
    assert a.unit <= a.unit


def test_gt():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'mm')
    assert a.unit > b.unit
    assert not a.unit > a.unit


def test_ge():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'mm')
    assert a.unit >= b.unit
    assert a.unit >= a.unit


def test_conversion_factor_to():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'mm')
    assert a.unit.conversion_factor_to(b.unit) == 1000


def test_conversion_tuple_to():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'mm')
    assert a.unit.conversion_tuple_to(b.unit) == (1000.0, 0.0)


def test_pow():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'm**2')
    assert a.unit**2 == b.unit
    assert b.unit**0.5 == a.unit


def test_is_angle():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'deg')
    c = PhysicalQuantity(1, 'rad')
    assert a.unit.is_angle == False
    assert b.unit.is_angle == True
    assert c.unit.is_angle == True


def test_latex():
    a = PhysicalQuantity(1, 'm')
    assert a.unit.latex == '$\\text{m}$'


def test_name():
    a = PhysicalQuantity(1, 'm')
    assert a.unit.name == 'm'


def test_isphysicalunit():
    a = PhysicalQuantity(1, 'm')
    assert isphysicalunit(a.unit) == True
    assert isphysicalunit(1) == False