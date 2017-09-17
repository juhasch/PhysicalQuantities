# -*- coding: utf-8 -*-
from nose.tools import raises

from PhysicalQuantities.decorator import *


def test_checkbaseunit_1():
    a = PhysicalQuantity(1, 'mm')
    assert checkbaseunit(a, 'm') == True


@raises(UnitError)
def test_checkbaseunit_2():
    a = 1
    assert checkbaseunit(a, 'm') == True


@raises(UnitError)
def test_checkbaseunit_3():
    a = PhysicalQuantity(1, 's')
    assert checkbaseunit(a, 'm') == True


def test_dropunit_1():
    a = PhysicalQuantity(1, 'm')
    assert dropunit(a, 'm') == a.value


def test_dropunit_2():
    a = PhysicalQuantity(1, 'm**2')
    assert dropunit(a, 'm**2') == a.value


@raises(UnitError)
def test_dropunit_3():
    a = PhysicalQuantity(1, 's')
    assert dropunit(a, 'm') == a.value


def test_require_units():
    u = PhysicalQuantity(2, 'V')
    i = PhysicalQuantity(3, 'A')
    w = PhysicalQuantity(1, 'W')
    @require_units('V', 'A')
    def power(u, i):
        return (u*i).W
    p = power(u, i)
    assert p.value == 6
    assert p.unit == w.unit


def test_optional_units():
    u = PhysicalQuantity(2, 'V')
    i = PhysicalQuantity(3, 'A')
    w = PhysicalQuantity(1, 'W')

    @optional_units('V', 'A', return_unit='W')
    def power(u, i):
        return u*i
    p = power(u, i)
    assert p.value == 6
    assert p.unit == w.unit
    p = power(u, 4)
    assert p.value == 8
    assert p.unit == w.unit
