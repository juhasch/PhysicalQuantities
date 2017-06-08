from PhysicalQuantities.ipython import _transform, init_match, init_dB_match


test_transformer = _transform().func
init_match()
init_dB_match()

def test_simple():
    """ No transformation """
    line = 'a = 0'
    ret = test_transformer(line)
    assert line == ret


def test_1():
    """ Simple unit """
    line = '1V'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(1,'V')"


def test_2():
    line = '1 V'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(1,'V')"


def test_3():
    line = '1 m/s'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(1,'m/s')"


def test_4():
    line = '1 km/h'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(1,'km/h')"


def test_5():
    """ Exponentials """
    line = '1 m**2'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(1,'m**2')"


def test_6():
    """ Don't convert strings"""
    line = "'1V'"
    ret = test_transformer(line)
    assert ret == "'1V'"


def test_7():
    line = '1V-2V'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(1,'V')-PhysicalQuantity(2,'V')"


def test_8():
    line = '1V/2m'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(1,'V')/PhysicalQuantity(2,'m')"


def test_9():
    line = '1e3 V'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(1e3,'V')"


def test_10():
    line = '1e-6 V'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(1e-6,'V')"


def test_pep15():
    line = '10_000 m'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(10000,'m')"


def test_pep15_dB():
    line = '10_000 dBm'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(10000,'dBm')"
