import json

import numpy as np
from nose.tools import raises

from PhysicalQuantities import PhysicalQuantity, units_html_list, units_list
from PhysicalQuantities.unit import (PhysicalUnit, UnitError,
                                     add_composite_unit, addunit, convertvalue,
                                     findunit, isphysicalunit)


def test_addunit_1():
    addunit(PhysicalUnit('degC', 1., [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], offset=273.15,
            url='https://en.wikipedia.org/wiki/Celsius', verbosename='degrees Celsius'))
    a = PhysicalQuantity(1, 'degC')
    assert(type(a.unit) == PhysicalUnit)


@raises(KeyError)
def test_addunit_2():
    addunit(PhysicalUnit('degC', 1., [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], offset=273.15,
            url='https://en.wikipedia.org/wiki/Celsius', verbosename='degrees Celsius'))
    addunit(PhysicalUnit('degC', 1., [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], offset=273.15,
            url='https://en.wikipedia.org/wiki/Celsius', verbosename='degrees Celsius'))


def test_add_composite_unit():
    add_composite_unit('test', 4.92892159375, 'cm**3')
    a = PhysicalQuantity(1, 'test')
    assert(type(a.unit) == PhysicalUnit)


@raises(KeyError)
def test_add_composite_unit_2():
    add_composite_unit('test', 4.92892159375, 'cm**3')
    add_composite_unit('test', 4.92892159375, 'cm**3')


def test_findunit_1():
    a = findunit('mm')
    b = PhysicalQuantity(1, 'mm').unit
    assert(a == b)


@raises(UnitError)
def test_findunit_2():
    findunit(0)


@raises(UnitError)
def test_findunit_3():
    findunit('xyz')


@raises(UnitError)
def test_findunit_4():
    findunit('')


@raises(UnitError)
def test_convertvalue():
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 'mm').unit
    convertvalue([1], a, b)


def test_unit_division_1():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(1, 'cm')
    assert type(a/b) == float


@raises(UnitError)
def test_unit_division_2():
    add_composite_unit('offsm', 1, 'm')
    a = PhysicalQuantity(1, 'offsm')
    b = PhysicalQuantity(1, 'm')
    a.unit.offset = 1
    a/b


def test_unit_multiplication_1():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(1, 'cm')
    assert str((a*b).base.unit) == "m^2"


@raises(UnitError)
def test_unit_multiplication_2():
    add_composite_unit('offsma', 1, 'm')
    a = PhysicalQuantity(1, 'offsma')
    b = PhysicalQuantity(1, 'm')
    a.unit.offset = 1
    a*b


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
    a = PhysicalQuantity(2, 'm')
    b = PhysicalQuantity(3, 'mm')
    assert a.unit.conversion_tuple_to(b.unit) == (1000.0, 0.0)


@raises(UnitError)
def test_conversion_tuple_to_2():
    # raises UnitError
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 's')
    assert a.unit.conversion_tuple_to(b.unit) == (1000.0, 0.0)


def test_isphysicalunit():
    a = PhysicalQuantity(1, 'm')
    assert isphysicalunit(a.unit) is True
    assert isphysicalunit(1) is False


def test_repr():
    a = PhysicalQuantity(1, 'm').unit
    b = a.__repr__()
    assert(b == '<PhysicalUnit m>')


def test_latex_repr():
    a = PhysicalQuantity(1, 'm').unit
    b = a.latex
    assert(b == r'\text{m}')


@raises(UnitError)
def test_gt_1():
    """Only same units can be compared"""
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 's').unit
    assert (a > b)


def test_gt_2():
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 'mm').unit
    assert (a > b)


@raises(UnitError)
def test_ge_1():
    """Only same units can be compared"""
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 's').unit
    assert (a >= b)


def test_ge_2():
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 'mm').unit
    assert (a >= b)


@raises(UnitError)
def test_lt_1():
    """Only same units can be compared"""
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 's').unit
    assert (a < b)


def test_lt_2():
    a = PhysicalQuantity(1, 'mm').unit
    b = PhysicalQuantity(1, 'm').unit
    assert (a < b)


@raises(UnitError)
def test_le_1():
    """Only same units can be compared"""
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 's').unit
    assert (a <= b)


def test_le_2():
    a = PhysicalQuantity(1, 'mm').unit
    b = PhysicalQuantity(1, 'm').unit
    assert (a <= b)


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
    addunit(PhysicalUnit('degX', 1., [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], offset=273.15))
    a = PhysicalQuantity(1, 'degX')
    a.unit.offset = 1.1
    a**2


def test_units_html_list():
    a = units_html_list()
    assert(len(a.data) > 1000)


def test_units_list():
    a,b = units_list()
    assert(len(a) > 10)


def test_to_dict():
    a = PhysicalQuantity(1, 'm')
    d = a.unit.to_dict
    assert type(d) is dict
    assert 'base_exponents' in d.keys()
    assert 'factor' in d.keys()
    assert 'offset' in d.keys()
    assert 'name' in d.keys()


def test_to_json():
    a = PhysicalQuantity(1, 'm')
    j = a.unit.to_json
    u = json.loads(j)
    assert type(u) is dict
    assert 'PhysicalUnit' in u.keys()
    d = u['PhysicalUnit']
    assert 'base_exponents' in d.keys()
    assert 'factor' in d.keys()
    assert 'offset' in d.keys()
    assert 'name' in d.keys()


def test_from_json():
    a = PhysicalQuantity(1, 'm')
    j = a.unit.to_json
    b = PhysicalUnit.from_json(j)
    assert a.unit == b
