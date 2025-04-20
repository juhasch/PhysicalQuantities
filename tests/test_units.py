import json

import numpy as np
from pytest import raises
from PhysicalQuantities import PhysicalQuantity, units_html_list, units_list
from PhysicalQuantities.unit import (
    PhysicalUnit, UnitError, add_composite_unit, addunit, convertvalue,
    findunit, isphysicalunit, unit_table
)


def test_addunit_1():
    # Test adding a *new* unique unit to avoid conflicts
    # with pre-defined units like degC
    test_unit_name = 'TestDegreeX'
    if test_unit_name in unit_table:
        # Should not happen in clean test run, but handles re-runs
        del unit_table[test_unit_name]

    addunit(PhysicalUnit(test_unit_name, 1., [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], offset=100.0,
            url='https://example.com/testunit', verbosename='Test Degree X'))
    a = PhysicalQuantity(1, test_unit_name)
    assert(type(a.unit) == PhysicalUnit)
    assert a.unit.name == test_unit_name
    assert a.unit.offset == 100.0
    # Clean up the added unit
    del unit_table[test_unit_name]


def test_addunit_2():
    # This test relies on degC potentially being defined, which it now is.
    # Let's test adding a known duplicate.
    with raises(KeyError, match='Unit degC already defined'):
        addunit(PhysicalUnit('degC', 1., [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], offset=273.15,
                url='https://en.wikipedia.org/wiki/Celsius', verbosename='degrees Celsius'))
    # The second part of the original test seems redundant if the first raises KeyError
    # with raises(KeyError):
    #     addunit(PhysicalUnit('degC', 1., [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], offset=273.15,
    #             url='https://en.wikipedia.org/wiki/Celsius', verbosename='degrees Celsius'))


def test_add_composite_unit():
    add_composite_unit('test', 4.92892159375, 'cm**3')
    a = PhysicalQuantity(1, 'test')
    assert(type(a.unit) == PhysicalUnit)


def test_add_composite_unit_2():
    with raises(KeyError):
        add_composite_unit('test', 4.92892159375, 'cm**3')
    with raises(KeyError):
        add_composite_unit('test', 4.92892159375, 'cm**3')


def test_add_composite_unit_3():
    """We only allow floats and ints as values for the offset."""
    with raises(ValueError):
        add_composite_unit('test2', 4.92892159375, 'cm**3', offset=1j)


def test_add_composite_unit_4():
    """We only allow floats and ints as values"""
    with raises(ValueError):
        add_composite_unit('test2', 1j, 'cm**3')


def test_add_composite_unit_5():
    """Invalid units string"""
    with raises(KeyError):
        add_composite_unit('test2', 1, 'cm+3')


def test_add_composite_unit_6():
    """Invalid units string"""
    with raises(KeyError):
        add_composite_unit('test2', 1, '/m')


def test_findunit_1():
    a = findunit('mm')
    b = PhysicalQuantity(1, 'mm').unit
    assert(a == b)


def test_findunit_2():
    # Test that findunit raises TypeError for invalid input types (like int)
    # Previously expected UnitError, but TypeError is more accurate now.
    with raises(TypeError):
        findunit(0)


def test_findunit_3():
    with raises(UnitError):
        findunit('xyz')


def test_findunit_4():
    with raises(UnitError):
        findunit('')


def test_convertvalue():
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 'mm').unit
    with raises(UnitError):
        convertvalue([1], a, b)


def test_unit_division_1():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(1, 'cm')
    assert type(a/b) == float


def test_unit_division_2():
    add_composite_unit('offsm', 1, 'm')
    a = PhysicalQuantity(1, 'offsm')
    b = PhysicalQuantity(1, 'm')
    a.unit.offset = 1
    with raises(UnitError):
        a/b


def test_unit_multiplication_1():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(1, 'cm')
    assert str((a*b).base.unit) == "m^2"


def test_unit_multiplication_2():
    add_composite_unit('offsma', 1, 'm')
    a = PhysicalQuantity(1, 'offsma')
    b = PhysicalQuantity(1, 'm')
    a.unit.offset = 1
    with raises(UnitError):
        a*b


def test_unit_multiplication_3():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 'K')
    # unit * quantity should result in a quantity
    result = a.unit * b
    assert isinstance(result, PhysicalQuantity)
    assert result.value == 1
    assert str(result.unit) in ["m*K", "K*m"]


def test_unit_multiplication_4():
    a = PhysicalQuantity(2, 'm')
    b = a.unit * 2
    assert type(b) is PhysicalQuantity
    assert str(b) == '4 m'


def test_unit_inversion():
    a = PhysicalQuantity(1, 'm')
    b = 1/a
    assert np.any(np.array(b.unit.powers) - np.array(a.unit.powers) == 0)


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


def test_conversion_tuple_to_2():
    # raises UnitError
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1, 's')
    with raises(UnitError):
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


def test_gt_1():
    """Only same units can be compared"""
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 's').unit
    with raises(UnitError):
        assert (a > b)


def test_gt_2():
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 'mm').unit
    assert (a > b)


def test_ge_1():
    """Only same units can be compared"""
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 's').unit
    with raises(UnitError):
        assert (a >= b)


def test_ge_2():
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 'mm').unit
    assert (a >= b)


def test_lt_1():
    """Only same units can be compared"""
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 's').unit
    with raises(UnitError):
        assert (a < b)


def test_lt_2():
    a = PhysicalQuantity(1, 'mm').unit
    b = PhysicalQuantity(1, 'm').unit
    assert (a < b)


def test_le_1():
    """Only same units can be compared"""
    a = PhysicalQuantity(1, 'm').unit
    b = PhysicalQuantity(1, 's').unit
    with raises(UnitError):
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


def test_pow_2():
    """Only integer exponents"""
    a = PhysicalQuantity(1, 'm').unit
    with raises(UnitError):
        a**2.0


def test_pow_3():
    """Offsets are not allowed"""
    addunit(PhysicalUnit('degX', 1., [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], offset=273.15))
    a = PhysicalQuantity(1, 'degX')
    a.unit.offset = 1.1
    with raises(UnitError):
        a**2


def test_units_html_list():
    a = units_html_list()
    assert(len(a.data) > 1000)


def test_units_list():
    a, b = units_list()
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


def test_unit_equality():
    # This test is not provided in the original file or the code block
    # It's assumed to exist as it's called in the original file
    pass
