import sys
import unittest
import numpy as np

from PhysicalQuantities.ipython import _transform, init_dB_match, init_match
from PhysicalQuantities import unit_table

test_transformer = _transform().func
init_match()
init_dB_match()

units_list = list(unit_table.keys())


# TODO: use sample, choices
def number_unit_generator():
    number_template = [f'1',
                       f'1.',
                       f'1.1',
                       f'1_00',
                       f'1_00.0_0',
                       f'1e3',
                       f'1.e3',
                       f'1e-3',
                       f'1.1e3',
                       f'1e-3',
                       ]

    i1 = np.random.randint(len(units_list))
    i2 = np.random.randint(len(units_list))
    u1 = units_list[i1]
    u2 = units_list[i2]
    unit_template = [f'{u1}',
                     f' {u1}**2',
                     f' {u1}/{u2}',
#                     f' {u1}/{u2}**2'
                     ]
    for nt in number_template:
        for ut in unit_template:
            number = nt
            unit = ut
            yield number, unit
    return 0, 0

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
    """Iterate through variations"""
    for number, unit in number_unit_generator():
        line = number + unit
        expected = f"PhysicalQuantity({number},'{unit.strip()}')"
        ret = test_transformer(line)
        print(line, '|',  expected, '|', ret)
        assert ret == expected


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

@unittest.skipIf(sys.version_info < (3, 6),
                    reason="requires python3.6")
def test_pep15():
    line = '10_000 m'
    ret = test_transformer(line)
    assert ret == "PhysicalQuantity(10_000,'m')"


@unittest.skipIf(sys.version_info < (3, 6),
                    reason="requires python3.6")
def test_pep15_dB():
    line = '10_000 dBm'
    ret = test_transformer(line)
    assert ret == "dBQuantity(10_000, 'dBm', islog=True)"
