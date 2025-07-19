import numpy as np
from PhysicalQuantities.quantity import PhysicalQuantity
from PhysicalQuantities import np_add_unit


def test_numpy_multiplication():
    a = np.array([1,1])
    b = PhysicalQuantity(1, 'm')
    assert str((a*b)[0].unit) == 'm'
    assert str((b*a)[0].unit) == 'm'    


def test_numpy_division():
    a = np.array([1,1])
    b = PhysicalQuantity(1, 'm')
    assert str((a/b)[0].unit) == '1/m'
    assert str((b/a)[0].unit) == 'm'


def test_indexing():
    a = np.arange(10) * PhysicalQuantity(1, 'm')
    b = a[0:2]
    assert (b.m_ == [0, 1]).all()


def test_np():
    a = PhysicalQuantity(np.random.rand(8), 'V')
    b = a.np
    assert isinstance(a.value, np.ndarray)
    assert isinstance(b, np.ndarray)
    metadata = b.dtype.metadata
    assert 'unit' in metadata
    assert metadata['unit'] == 'V'


def test_np_add_unit():
    a = np.random.rand(8)
    b = np_add_unit(a, 'V')
    metadata = b.dtype.metadata
    assert 'unit' in metadata
    assert metadata['unit'] == 'V'
