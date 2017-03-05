from PhysicalQuantities import PhysicalQuantity
from numpy.testing import assert_almost_equal


def test_complex_assign():
    """ wrap complex number with quantity """
    a = (1+2j) * PhysicalQuantity(1,'V')
    assert str(a) == '(1+2j) V'


def test_complex_attr():
    """ test getting real/imaginary part 
        real/imag attributes of complex numbers always return floats...
    """
    a = (1.0+2.0j) * PhysicalQuantity(1,'V')
    assert str(a.real) == '1.0 V'
    assert str(a.imag) == '2.0 V'


def test_complex_mag():
    """ Test magnitude computation """
    a = (1+2j) * PhysicalQuantity(1,'V')
    b = abs(a)
    assert_almost_equal(b.value, ((a.real**2 +a.imag**2)**0.5).value)
