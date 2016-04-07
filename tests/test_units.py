# -*- coding: utf-8 -*-
from PhysicalQuantities import PhysicalQuantity
from PhysicalQuantities.Unit import isphysicalunit, UnitError, findunit, convertvalue, units_html_list
import numpy as np
from nose.tools import raises


def test_findunit_1():
    a = findunit('mm')
    b = PhysicalQuantity(1, 'mm').unit
    assert(a == b)


@raises(UnitError)
def test_findunit_2():
    findunit(0)


@raises(UnitError)
def test_findunit_2():
    findunit(0)


@raises(UnitError)
def test_convertvalue():
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 'mm').unit
    convertvalue([1], a, b)


def test_unit_division_2():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(1, 'cm')
    assert type(a/b) == float


def test_unit_multiplication():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(1, 'cm')
    assert str((a*b).base.unit) == "m^2"


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


def test_conversion_factor_to():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'mm')
    assert a.unit.conversion_factor_to(b.unit) == 1000


def test_conversion_tuple_to():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'mm')
    assert a.unit.conversion_tuple_to(b.unit) == (1000.0, 0.0)


@raises(UnitError)
def test_conversion_tuple_to_2():
    # raises UnitError
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 's')
    assert a.unit.conversion_tuple_to(b.unit) == (1000.0, 0.0)


def test_isphysicalunit():
    a = PhysicalQuantity(1, 'm')
    assert isphysicalunit(a.unit) == True
    assert isphysicalunit(1) == False


def test_repr():
    a = PhysicalQuantity(1, 'm').unit
    b = a.__repr__()
    assert(b == '<PhysicalUnit m>')


def test_latex_repr():
    a = PhysicalQuantity(1, 'm').unit
    b = a.latex
    assert(b == r'\text{m}')


@raises(UnitError)
def test_gt():
    """Only same units can be compared"""
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 's').unit
    assert (a > b is True)


@raises(UnitError)
def test_ge():
    """Only same units can be compared"""
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 's').unit
    assert (a >= b is True)


@raises(UnitError)
def test_lt():
    """Only same units can be compared"""
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 's').unit
    assert (a < b is True)


def test_pow_1():
    """Only integer exponents"""
    a = PhysicalQuantity(1, 'm^2').unit
    b = PhysicalQuantity(1, 'm').unit
    assert(a**0.5 == b)


@raises(UnitError)
def test_pow_2():
    """Only integer exponents"""
    a = PhysicalQuantity(1, 'm').unit
    a**2.0


@raises(UnitError)
def test_pow_3():
    """Offsets are not allowed"""
    a = PhysicalQuantity(1, 'm').unit
    a.offset = 1
    a**2


def test_units_html_list():
    a = units_html_list()
    assert(len(a.data) > 1000)
