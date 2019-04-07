
from IPython import __version__
from PhysicalQuantities import unit_table

if __version__ < '7.0.0':
    from PhysicalQuantities.ipython import transform_legacy
    test_transformer = transform_legacy().func
else:
    from PhysicalQuantities.ipython import transform_line
    test_transformer = transform_line

units_list = list(unit_table.keys())


def test_simple():
    """ No transformation """
    line = 'a =0'
    ret = test_transformer(line).strip()
    assert line == ret


def test_1():
    """ Simple unit """
    line = '1V'
    ret = test_transformer(line).strip()
    assert ret == "(1 *pq.V)"


def test_6():
    """ Don't convert strings"""
    line = "'1V'"
    ret = test_transformer(line).strip()
    assert ret == "'1V'"


def test_7():
    line = '1V-2V'
    ret = test_transformer(line).strip()
    assert ret == "(1 *pq.V) -(2 *pq.V)"


def test_8():
    """Divide unit quantities"""
    line = '1V/2m'
    ret = test_transformer(line).strip()
    assert ret == "(1 *pq.V) /(2 *pq.m)"


def test_9():
    """Combined dimension"""
    line = '1m/s'
    ret = test_transformer(line).strip()
    assert ret == "(1 *pq.m) / pq.s"


def test_10():
    """Test exponentials"""
    line = '10m**2'
    ret = test_transformer(line).strip()
    assert ret == 'PhysicalQuantity(10 ,"m**2")'


def test_multiline_comment():
    """Make sure multiline comments are handled properly"""
    lines = '"""\n2m"""'
    ret = test_transformer(lines).strip()
    assert ret == lines

