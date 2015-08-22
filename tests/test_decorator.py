# -*- coding: utf-8 -*-
import PhysicalQuantities as pq
from PhysicalQuantities.decorator import *
import numpy as np


def test_checkbaseunit():
    a = PhysicalQuantity(1, 'mm')
    assert checkbaseunit(a, 'm') == True


def test_dropunit():
    a = PhysicalQuantity(1, 'm')
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
