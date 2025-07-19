import copy

import numpy as np
from numpy.testing import assert_almost_equal
from pytest import raises
from IPython.core.formatters import PlainTextFormatter
from PhysicalQuantities import PhysicalQuantity
from PhysicalQuantities.dBQuantity import PhysicalQuantity_to_dBQuantity, dB10, dB20, dBQuantity
from PhysicalQuantities.unit import UnitError


def test_name():
    a = dBQuantity(1, 'dBm')
    assert a.unit.__name__ == 'dBm'


def test_init():
    with raises(UnitError):
        a = dBQuantity(1, 'x')


def test_basic_properties_1():
    """ test value attribute """
    g = dBQuantity(0.1, 'dBm')
    assert g.value == 0.1


def test_basic_properties_2():
    """ test unit attribute """
    g = dBQuantity(0.1, 'dBm')
    assert g.unit.name == 'dBm'


def test_basic_properties_3():
    """ test log10 factor """
    g = dBQuantity(0.1, 'dBm')
    assert g.unit.factor == 10


def test_basic_properties_4():
    """ test default impedance """
    g = dBQuantity(0.1, 'dBm')
    assert g.unit.z0 == PhysicalQuantity(50, 'Ohm')


def test_basic_properties_5():
    """ test conversion back to linear """
    g = dBQuantity(0.1, 'dBm')
    assert_almost_equal(g.lin.value, 1.023292992280754)


def test_conversion_1():
    """ test conversion back to linear using attribute """
    g = dBQuantity(0, 'dBm')
    glin = PhysicalQuantity(1, 'mW')
    assert g.mW == glin


def test_conversion_2():
    """ test conversion back to linear using attribute """
    g = dBQuantity(0, 'dBm')
    glin = PhysicalQuantity(1, 'mW')
    assert g.mW_ == 1


def test_conversion_3():
    """ test conversion back to linear using attribute """
    g = dBQuantity(0, 'dBm')
    glin = PhysicalQuantity(1, 'mW')
    assert g.dBW_ == -30
    

def test_conversion_4():
    """ test conversion back to linear using attribute """
    g = dBQuantity(0, 'dBm')
    glin = PhysicalQuantity(1, 'mW')
    assert g.W_ == 0.001


def test_gt_dB():
    """ test gt operator """
    g1 = dBQuantity(0, 'dB')
    g2 = dBQuantity(1, 'dB')
    g3 = dBQuantity(-1, 'dB')
    assert g1 > g3
    assert g2 > g3
    assert not g3 > g1


def test_gt_dB_1():
    """ test gt operator with units """
    g1 = dBQuantity(1, 'dBV')
    g2 = dBQuantity(-1, 'dBV')
    assert g1 > g2


def test_gt_dB_2():
    """ test gt operator with different units """
    g2 = dBQuantity(1, 'dBnV')
    g3 = dBQuantity(1, 'dBmV')
    assert g3 > g2


def test_gt_dB_3():
    """ test eq operator with scalar """
    g = dBQuantity(0, 'dBnV')
    with raises(UnitError):
        assert g > 0


def test_gt_dB_4():
    """ test eq operator with different dB unit """
    g1 = dBQuantity(0, 'dBV')
    g2 = dBQuantity(0, 'dBW')
    with raises(UnitError):
        assert g1 > g2


def test_lt_dB():
    """ test lt operator """
    g1 = dBQuantity(0, 'dB')
    g2 = dBQuantity(1, 'dB')
    g3 = dBQuantity(-1, 'dB')
    assert g1 < g2
    assert g3 < g2
    assert not g1 > g2


def test_lt_dB_1():
    """ test lt operator with units """
    g1 = dBQuantity(1, 'dBV')
    g2 = dBQuantity(-1, 'dBV')
    assert g2 < g1


def test_lt_dB_2():
    """ test lt operator with different units """
    g2 = dBQuantity(1, 'dBnV')
    g3 = dBQuantity(1, 'dBmV')
    assert g2 < g3


def test_lt_dB_3():
    """ test lt operator with scalar """
    g = dBQuantity(0, 'dBnV')
    with raises(UnitError):
        assert g < 0


def test_lt_dB_4():
    """ test lt operator with different dB unit """
    g1 = dBQuantity(0, 'dBV')
    g2 = dBQuantity(0, 'dBW')
    with raises(UnitError):
        assert g1 < g2


def test_eq_dB():
    """ test eq operator """
    g1 = dBQuantity(0, 'dB')
    g2 = dBQuantity(1, 'dB')
    assert g1 == g1
    assert not g1 == g2


def test_eq_dB_1():
    """ test eq operator with units """
    g1 = dBQuantity(0, 'dBV')
    g2 = dBQuantity(1, 'dBV')
    assert g1 == g1
    assert not g1 == g2


def test_eq_dB_2():
    """ test eq operator with different units """
    g1 = dBQuantity(0, 'dBnV')
    g2 = dBQuantity(1, 'dBmV')
    assert g1 == g1
    assert not g1 == g2


def test_eq_dB_3():
    """ test eq operator with scalar """
    g = dBQuantity(0, 'dBnV')
    # Comparing dBQuantity with scalar should be False
    assert (g == 0) is False


def test_eq_dB_4():
    """ test eq operator with different dB unit """
    g1 = dBQuantity(0, 'dBV')
    g2 = dBQuantity(0, 'dBW')
    with raises(UnitError):
        assert g1 == g2


def test_ne_db():
    """ test ne operator """
    g1 = dBQuantity(0, 'dB')
    g2 = dBQuantity(1, 'dB')
    assert g1 != g2
    assert not g1 != g1


def test_ne_db_1():
    """ test ne operator with units """
    g1 = dBQuantity(0, 'dBV')
    g2 = dBQuantity(1, 'dBV')
    assert g1 != g2
    assert not g1 != g1


def test_ne_db_2():
    """ test ne operator with different units """
    g1 = dBQuantity(0, 'dBmV')
    g2 = dBQuantity(1, 'dBnV')
    assert g1 != g2
    assert not g1 != g1


def test_ne_dB_3():
    """ test eq operator with scalar """
    g = dBQuantity(0, 'dBnV')
    # Comparing dBQuantity with scalar should be True for !=
    assert (g != 0) is True


def test_ne_dB_4():
    """ test ne operator with different dB unit """
    g1 = dBQuantity(0, 'dBV')
    g2 = dBQuantity(0, 'dBW')
    with raises(UnitError):
        assert g1 != g2


def test_ge_dB():
    """ test ge operator """
    g1 = dBQuantity(0, 'dB')
    g2 = dBQuantity(1, 'dB')
    g3 = dBQuantity(-1, 'dB')
    assert g2 >= g1
    assert g1 >= g1
    assert not g3 >= g1


def test_ge_dB_1():
    """ test ge operator with units"""
    g1 = dBQuantity(0, 'dBV')
    g2 = dBQuantity(1, 'dBV')
    assert g2 >= g1


def test_ge_dB_2():
    """ test ge operator with different units"""
    g1 = dBQuantity(1, 'dBnV')
    g2 = dBQuantity(1, 'dBmV')
    assert g2 >= g1


def test_ge_dB_3():
    """ test eq operator with scalar """
    g = dBQuantity(0, 'dBnV')
    with raises(UnitError):
        assert g >= 0


def test_ge_dB_4():
    """ test ge operator with different dB unit """
    g1 = dBQuantity(0, 'dBV')
    g2 = dBQuantity(0, 'dBW')
    with raises(UnitError):
        assert g1 >= g2


def test_le_dB_1():
    """ test le operator """
    g1 = dBQuantity(0, 'dB')
    g2 = dBQuantity(1, 'dB')
    g3 = dBQuantity(-1, 'dB')
    assert g3 <= g3
    assert g3 <= g1
    assert not g2 <= g1


def test_le_dB_2():
    """ test le operator with different units"""
    g1 = dBQuantity(1, 'dBnV')
    g2 = dBQuantity(1, 'dBmV')
    assert g1 <= g2
    
    

def test_le_dB_3():
    """ test le operator with different dB unit """
    g1 = dBQuantity(0, 'dBV')
    g2 = dBQuantity(0, 'dBW')
    with raises(UnitError):
        assert g1 <= g2


def test_le_dB_4():
    """ test eq operator with scalar """
    g = dBQuantity(0, 'dBnV')
    with raises(UnitError):
        assert g <= 0


def test_lin_1():
    a = dBQuantity(6, 'dBV')
    b = a.lin
    assert_almost_equal(b.dB.value, a._)


def test_lin_2():
    a = dBQuantity(6, 'dB')
    with raises(UnitError):
        a.lin


def test_lin10_1():
    a = dBQuantity(6, 'dB')
    b = a.lin10
    assert_almost_equal(b, 3.9810717055349722)


def test_lin10_2():
    a = dBQuantity(6, 'dBm')
    b = a.lin10
    assert_almost_equal(b.value, 3.9810717055349722)


def test_lin10_3():
    a = dBQuantity(6, 'dBV')
    with raises(ValueError):
        b = a.lin10


def test_lin20():
    a = dBQuantity(6, 'dB')
    b = a.lin20
    assert_almost_equal(b, 1.9952623149688795)


def test_lin20_2():
    a = dBQuantity(6, 'dBV')
    b = a.lin20
    assert_almost_equal(b.value, 1.9952623149688795)


def test_lin20_3():
    a = dBQuantity(6, 'dBm')
    with raises(ValueError):
        b = a.lin20


def test_calculation_1():
    """ test addition """
    g = dBQuantity(0, 'dBm')
    a = dBQuantity(10, 'dB')
    ga = dBQuantity(10, 'dBm')
    assert a + g == ga
    assert g + a == ga


def test_calculation_2():
    """ test addition """
    g = dBQuantity(0, 'dBm')
    a = dBQuantity(0, 'dBm')
    ga = PhysicalQuantity(2, 'mW').dB
    assert a + g == ga
    assert g + a == ga


def test_numpy_dB():
    a = np.array([1., 2., 3.])
    b = a * PhysicalQuantity(1, 'V')
    c = b.dB
    assert_almost_equal(c.lin.value, a)


def test_add_db_1():
    g1 = dBQuantity(1,'dB')
    g2 = dBQuantity(2,'dB')
    assert (g1 + g2).value == 3


def test_add_db_2():
    g1 = dBQuantity(0, 'dBm')
    g2 = dBQuantity(0, 'dBm')
    assert_almost_equal((g1 + g2).value, 3.0102999566398121)


def test_sub_db_1():
    g1 = dBQuantity(1,'dB')
    g2 = dBQuantity(2,'dB')
    assert (g1 - g2).value == -1


def test_sub_db_2():
    g1 = dBQuantity(1, 'dBm')
    g2 = dBQuantity(0, 'dBm')
    assert_almost_equal((g1 - g2).value, -5.8682532438011537)


def test_sub_db_3():
    g1 = dBQuantity(1, 'dBm')
    g2 = dBQuantity(0, 'dBV')
    with raises(UnitError):
        g1 - g2


def test_dB10_0():
    a = dB10(PhysicalQuantity(10, 'V'))
    assert a.value == 10


def test_dB10_1():
    a = dB10(100)
    b = dB10(0.1)
    assert a.value == 20
    assert b.value == -10


def test_dB20():
    a = dB20(PhysicalQuantity(10, 'V'))
    assert a.value == 20


def test_dB20_1():
    a = dB20(100)
    b = dB20(0.1)
    assert a.value == 40
    assert b.value == -20


def test_getitem_1():
    a = np.ones(2) * dBQuantity(1, 'dBm')
    assert a[0].value == 1.0


def test_getitem_2():
    a = dBQuantity(1, 'dBm')
    with raises(AttributeError):
        assert a[0].value == 1.0


def test_setitem_1():
    a = np.ones(2) * dBQuantity(1, 'dBm')
    a[0] = dBQuantity(2, 'dBm')
    assert a[0] == dBQuantity(2, 'dBm')


def test_setitem_2():
    a = dBQuantity(1, 'dBm')
    with raises(AttributeError):
        a[0] = 1


def test_to_dB_0():
    a = PhysicalQuantity(1, 'mV')
    assert a.dB.unit.name == 'dBmV'


def test_to_dB_1():
    a = PhysicalQuantity(1, 'V')
    assert a.dB.value == 0.0


def test_to_dB_2():
    a = PhysicalQuantity(1, 'V')
    assert a.dB.dBV.value == 0.0


def test_to_dB_3():
    a = PhysicalQuantity(1, 'V')
    assert a.dB.dBmV.value == 60.0


def test_to_dB_4():
    a = PhysicalQuantity(1, 'V')
    assert a.dB.dBuV.value == 120.0


def test_floordiv():
    a = dBQuantity(4, 'dB')
    b = 2
    c = a // b
    assert c.value == 2


def test_floordiv_exc():
    """ Division of dBx units is illegal"""
    a = dBQuantity(4, 'dB')
    b = dBQuantity(2, 'dB')
    with raises(UnitError):
        c = a // b


def test_rfloordiv():
    a = 4
    b = dBQuantity(2, 'dB')
    c = a // b
    assert c.value == 2


def test_getattr():
    a = dBQuantity(0, 'dBm')
    b = dBQuantity(-30, 'dBW')
    assert a.dBm == a
    assert a.dBW == b
    assert a.dBm_ == 0
    assert_almost_equal(a.dBm_, b.dBm_)
    assert_almost_equal(a.dBW_, -30)


def test_getattr2():
    a = dBQuantity(3, 'dB')
    assert a._ == 3


def test_PhysicalQuantity_to_dBQuantity():
    a = PhysicalQuantity(2, 'V')
    b = PhysicalQuantity_to_dBQuantity(a, 'dBuV')
    assert_almost_equal(b.value, 126.02059991327963)


def test_PhysicalQuantity_to_dBQuantity_1():
    with raises(UnitError):
        a = PhysicalQuantity(2, 'm')
        b = PhysicalQuantity_to_dBQuantity(a)


def test_PhysicalQuantity_to_dBQuantity_2():
    with raises(UnitError):
        b = PhysicalQuantity_to_dBQuantity(1, 'dBuV')


def test_dB():
    a = dBQuantity(0, 'dBm')
    assert(str(a.dB) == '0 dB')


def test_div_1():
    a = dBQuantity(4, 'dB')
    b = a / 4
    assert_almost_equal(b.value, 1)


def test_div_2():
    a = dBQuantity(4, 'dBm')
    with raises(UnitError):
        b = a / 4


def test_len_db_1():
    a = [dBQuantity(4, 'dBm')]
    assert(len(a) == 1)


def test_len_db_2():
    a = dBQuantity(4, 'dBm')
    with raises(TypeError):
        assert(len(a) == 1)


def test_len_db_3():
    a = np.ones(2) * dBQuantity(4, 'dBm')
    assert(len(a) == 2)


def test_to_db():
    a = dBQuantity(4, 'dBm')
    b = a.to('dBW')
    assert_almost_equal(a.lin.W_, b.lin.W_)


def test_indexing_db_1():
    a = [dBQuantity(4, 'dBm')]
    assert(a[0].value == 4)


def test_indexing_db_2():
    a = [dBQuantity(4, 'dBm')]
    with raises(IndexError):
        assert(a[1].value == 4)


def test_dir_db():
    a = dBQuantity(4, 'dBm')
    b = list(a.__dir__())
    assert('dB' in b)


def test_dBi_to_lin():
    a = dBQuantity(20, 'dBi')
    assert(a.lin == 100.0)


def test_dBd_to_dBi():
    a = dBQuantity(20, 'dBd')
    b = a.dBi
    assert(b.value == 22.15)


def test_dBsm_to_m2():
    a = dBQuantity(20, 'dBsm')
    b = a.lin
    assert(b.unit.name == 'm**2')
    assert(b.value == 100)


def test_m2_to_dBsm():
    a = PhysicalQuantity(100, 'm**2')
    b = a.dB
    assert(b.unit.name == 'dBsm')
    assert(b.value == 20)


def test_repr():
    a = dBQuantity(0, 'dBm')
    assert a.__repr__() == '0 dBm'


def test_db10():
    a = PhysicalQuantity(1, 'mW')
    b = dB10(a)
    assert b.value == -30


def test_db10_val():
    b = dB10(1e-3)
    assert b.value == -30


def test_db20():
    a = PhysicalQuantity(1, 'mV')
    b = dB20(a)
    assert b.value == -60


def test_db20_val():
    b = dB20(1e-3)
    assert b.value == -60


def test_deepcopy():
    a = dBQuantity(1, 'dBm')
    b = copy.deepcopy(a)
    assert a == b
    assert a is not b


def test_neg():
    a = dBQuantity(1, 'dBm')
    b = dBQuantity(-1, 'dBm')
    assert a == -b


def test_ip_str():
    """IPython formatter"""
    a = dBQuantity(1.0, 'dBm')
    a.ptformatter = PlainTextFormatter()
    a.format = ''
    assert str(a) == '1.0 dBm'


def test_add_unequal():
    a = dBQuantity(1, 'dBm')
    b = dBQuantity(1, 'dBV')
    with raises(UnitError):
        a + b


def test_getitem():
    b = dBQuantity(1, 'dBV')
    with raises(AttributeError):
        assert b[0] == 0


def test_setitem():
    b = dBQuantity(1, 'dBV')
    with raises(AttributeError):
        b[0] = 0
