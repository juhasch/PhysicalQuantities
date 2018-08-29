"""Test __init__.py """

import PhysicalQuantities as pq
from PhysicalQuantities.quantity import PhysicalQuantity
from PhysicalQuantities.unit import PhysicalUnit
from PhysicalQuantities.quantityarray import PhysicalQuantityArray


def test_q():
    assert pq.Q is PhysicalQuantity


def test_u():
    assert pq.U is PhysicalUnit


def test_qa():
    assert pq.QA is PhysicalQuantityArray


def test_quantity_item():
    assert type(pq.q['m']) is PhysicalQuantity


def test_quantity_getattr():
    assert type(pq.q.m) is PhysicalQuantity


def test_quantity_dir():
    d = pq.q.__dir__()
    assert len(d) > 40

