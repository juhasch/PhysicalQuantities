from PhysicalQuantities.fractdict import *


def test_getitem():
    a = FractionalDict()
    a['a'] = 1
    assert a['a'] == 1


def test_create():
    """ create ndict from dict """
    a = {'a': 1}
    b = FractionalDict(a)
    assert a == b


def test_add():
    a = FractionalDict()
    a['a'] = 1
    b = FractionalDict()
    b['a'] = 2
    b['b'] = 2
    c = {'a': 3, 'b': 2}
    assert a+b == c


def test_sub():
    a = FractionalDict()
    a['a'] = 1
    b = FractionalDict()
    b['a'] = 2
    b['b'] = 2
    c = {'a': -1, 'b': -2}
    assert a-b == c


def test_mul_1():
    a = FractionalDict({'a': 3, 'b': 2})
    b = Fraction(2)
    c = a*b
    assert c['a'] == 3*2
    assert c['b'] == 2*2


def test_div():
    a = FractionalDict({'a': 3, 'b': 2})
    c = Fraction(3)
    b = a//c
    assert b['a'] == Fraction(3, 3)
    assert b['b'] == Fraction(2, 3)


def test_rdiv():
    a = FractionalDict({'a': 3, 'b': 2})
    b = Fraction(3)/a
    assert b['a'] == Fraction(3, 3)
    assert b['b'] == Fraction(3, 2)


def test_truediv():
    a = FractionalDict({'a': 3, 'b': 2})
    b = a/Fraction(3)
    assert b['a'] == Fraction(3, 3)
    assert b['b'] == Fraction(2, 3)


def test_floordiv():
    a = FractionalDict({'a': 3, 'b': 6})
    b = a//Fraction(3)
    assert b['a'] == 1
    assert b['b'] == 2


def test_rfloordiv():
    a = FractionalDict({'a': 2, 'b': 3})
    b = Fraction(6)//a
    assert b['a'] == 3
    assert b['b'] == 2


def test_rmul():
    a = FractionalDict({'a': 3, 'b': 2})
    b = Fraction(2)*a
    assert b['a'] == 2*3
    assert b['b'] == 2*2
