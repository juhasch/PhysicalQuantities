import PhysicalQuantities as pq


def test_exp_0():
    """ exponentials can be given in several forms """
    a = pq.Q(1.0,'m**2')
    b = pq.Q(1.0,'m^2')    
    c = pq.Q(1.0,'m')**2
    assert a == b
    assert a == c


def test_exp_1():
    """ exponentials can be given in two forms """
    a = pq.Q(1.0,'m**2')
    assert str(a) == '1.0 m^2'


def test_exp_2():
    """ test square root """
    a = pq.Q(1.0,'m')**2
    assert str(a**0.5) == '1.0 V'


def test_exp_3():
    """ exponentials in numerator and denominator """
    a = pq.Q(1.0,'m**2/s**4')
    assert a == '1.0 m^2/s^4'


def text_exp_4():
    """ test square root """
    a = pq.Q(4.0,'m**2/s**4')
    assert a == '2.0 m/s^2.0'
