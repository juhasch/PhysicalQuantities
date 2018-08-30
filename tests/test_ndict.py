from PhysicalQuantities.NDict import *


def test_getitem():
    a = NumberDict()
    a['a'] = 1
    assert a['a'] == 1


def test_create():
    """ create ndict from dict """
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
    a = NumberDict({'a' : 3, 'b': 2})
    b = 2*a
    assert b['a'] == 2*3
    assert b['b'] == 2*2


def test_div():
    a = NumberDict({'a' : 3, 'b': 2})
    b = a/3
    assert b['a'] == 3.0/3.0
    assert b['b'] == 2.0/3.0


def test_rdiv():
    a = NumberDict({'a' : 3, 'b': 2})
    b = 3/a
    assert b['a'] == 3.0/3.0
    assert b['b'] == 3.0/2.0


def test_floordiv():
    a = NumberDict({'a' : 3, 'b': 6})
    b = a//3
    assert b['a'] == 1
    assert b['b'] == 2


def test_rfloordiv():
    a = NumberDict({'a' : 2, 'b': 3})
    b = 6//a
    assert b['a'] == 3
    assert b['b'] == 2
