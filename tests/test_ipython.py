import sys
import unittest
import numpy as np

from PhysicalQuantities.ipython import _transform
from PhysicalQuantities import unit_table

test_transformer = _transform().func

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
    assert ret == "1 * pq.V"


def test_6():
    """ Don't convert strings"""
    line = "'1V'"
    ret = test_transformer(line).strip()
    assert ret == "'1V'"


def test_7():
    line = '1V-2V'
    ret = test_transformer(line).strip()
    assert ret == "1 * pq.V -2 * pq.V"


def test_8():
    """Divide unit quantities"""
    line = '1V/2m'
    ret = test_transformer(line).strip()
    assert ret == "1 * pq.V /2 * pq.m"


def test_9():
    """Combined dimension"""
    line = '1m/s'
    ret = test_transformer(line).strip()
    assert ret == "1 * pq.m / pq.s"
