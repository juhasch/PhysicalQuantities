# -*- coding: utf-8 -*-
from PhysicalQuantities.NDict import *


def test_getitem():
    a = NumberDict()
    a['a'] = 1
    assert a['a'] == 1


def test_coerce():
    a = {'a': 1}
    b = NumberDict(a)
    assert a == b


def test_add():
    a = NumberDict()
    a['a'] = 1
    b = NumberDict()
    b['a'] = 2
    b['b'] = 2
    c = {'a' : 3, 'b': 2}
    assert a+b == c


def test_sub():
    a = NumberDict()
    a['a'] = 1
    b = NumberDict()
    b['a'] = 2
    b['b'] = 2
    c = {'a' : -1, 'b': -2}
    assert a-b == c


def test_mul():
    a = NumberDict()
    a['a'] = 1
    b = 2*a['a']
    assert b == 2


def test_div():
    a = NumberDict()
    a['a'] = 2
    assert a['a']/2 == 1


def test_rdiv():
    a = NumberDict()
    a['a'] = 2
    assert 2/a['a'] == 1
