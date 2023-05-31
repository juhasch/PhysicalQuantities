
from PhysicalQuantities import unit_table
from PhysicalQuantities.ipython import transform


def test_empty():
    """ Single line """
    line = []
    ret = transform(line)
    assert line == ret


def test_single():
    """ Single line """
    line = ['a =0']
    ret = transform(line)
    assert line == ret


def test_multi():
    """ Multi line """
    line = ['a=1V', 'b = 1']
    ret = transform(line)
    assert ret[0] == "a=(1 *pq.V) "


def test_comment():
    """ Multi line """
    line = [' """ ', 'a=1V', ' """ ']
    ret = transform(line)
    assert ret[1] == "a=1V"
