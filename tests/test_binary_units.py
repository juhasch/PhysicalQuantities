from PhysicalQuantities import PhysicalQuantity
import PhysicalQuantities.binary_units


def test_bit():
    a = PhysicalQuantity(1, 'KiBit')
    assert str(a.base) == '1024 Bit'


def test_byte():
    a = PhysicalQuantity(1, 'KiByte')
    assert str(a.base) == '8192 Bit'


def test_floordiv():
    a = PhysicalQuantity(1, 'KiBit')
    b = PhysicalQuantity(1, 'KiByte')
    assert b//a == 8
