# -*- coding: utf-8 -*-
from PhysicalQuantities.Quantity import PhysicalQuantity, isphysicalquantity
from numpy.testing import assert_almost_equal


def test_isphysicalquantity():
    g = PhysicalQuantity(1, 'mm')
    assert isphysicalquantity(g) is True
    assert isphysicalquantity(1) is False


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


def test_decorators():
    """ Test .base and .value decorators """
    g=PhysicalQuantity(98, 'mm')/ PhysicalQuantity(1, 's**2')
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


def test_repr_latex():
    b = PhysicalQuantity(1, 'mm')
    assert b._repr_latex_() == '1 $\\text{mm}$'


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


def test_div():
    a = PhysicalQuantity(3, 'mm**2')
    b = PhysicalQuantity(4, 'mm')
    assert a/b == PhysicalQuantity(3/4, 'mm')
    assert b/b == 1


def test_pow():
    a = PhysicalQuantity(4, 'mm')
    b = PhysicalQuantity(16, 'mm**2')
    assert pow(a, 2) == b


def test_eq():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(2, 'mm')
    assert a == a
    assert not a == b


def test_ne():
    a = PhysicalQuantity(1, 'mm')
    b = PhysicalQuantity(2, 'mm')
    assert a != b
    assert not a != a


def test_lt():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(2, 'm')
    assert a < b
    assert not a < a


def test_le():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(2, 'm')
    assert a <= b
    assert a <= a


def test_gt():
    a = PhysicalQuantity(2, 'm')
    b = PhysicalQuantity(1, 'm')
    assert a > b
    assert not a > a


def test_ge():
    a = PhysicalQuantity(2, 'm')
    b = PhysicalQuantity(1, 'm')
    assert a >= b
    assert a >= a


def test_to():
    a = PhysicalQuantity(1, 'm')
    b = PhysicalQuantity(1000, 'mm')
    assert a.to('mm') == b


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


def test_pow():
    a = PhysicalQuantity(2, 'm')
    b = PhysicalQuantity(4, 'm**2')
    assert a.pow(2) == b
    assert a**2 == b


def test_sqrt():
    a = PhysicalQuantity(2, 'm')
    b = PhysicalQuantity(4, 'm**2')
    assert b.pow(0.5) == a
    assert b**0.5 == a


def test_autoscale():
    """ Unit autoscaling """
    a = PhysicalQuantity(1e-3, 'm')
    b = a.autoscale
    assert str(a.mm) == str(b)
    a = PhysicalQuantity(1e3, 'm')
    b = a.autoscale
    assert str(a.km) == str(b)


def test_any_to():
    pass # TODO


def test_format():
    a = PhysicalQuantity(1.123123, 'm')
    assert str(a) == '1.123123 m'
    a.format = '.3f'
    assert str(a) == '1.123 m'
