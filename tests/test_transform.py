
from PhysicalQuantities import unit_table

from PhysicalQuantities.transform import transform_line

units_list = list(unit_table.keys())


def test_simple():
    """ No transformation """
    line = 'a =0'
    ret = transform_line(line).strip()
    assert line == ret


def test_1():
    """ Simple unit """
    line = '1V'
    ret = transform_line(line).strip()
    assert ret == "(1 *pq.V)"


def test_6():
    """ Don't convert strings"""
    line = "'1V'"
    ret = transform_line(line).strip()
    assert ret == "'1V'"


def test_7():
    line = '1V-2V'
    ret = transform_line(line).strip()
    assert ret == "(1 *pq.V) -(2 *pq.V)"


def test_8():
    """Divide unit quantities"""
    line = '1V/2m'
    ret = transform_line(line).strip()
    assert ret == "(1 *pq.V) /(2 *pq.m)"


def test_9():
    """Combined dimension"""
    line = '1m/s'
    ret = transform_line(line).strip()
    assert ret == "(1 *pq.m) / pq.s"


def test_10():
    """Test exponentials"""
    line = '10m**2'
    ret = transform_line(line).strip()
    assert ret == 'PhysicalQuantity(10 ,"m**2")'


def test_multiline_comment():
    """Make sure multiline comments are handled properly"""
    lines = '"""\n2m"""'
    ret = transform_line(lines).strip()
    assert ret == lines
