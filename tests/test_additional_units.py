from PhysicalQuantities import q
from PhysicalQuantities.more_units import *


def test_d():
    assert(q.d.unit.verbosename == 'day')


def test_yr():
    assert(q.yr.unit.verbosename == 'year')


def test_fortnight():
    assert(q.fortnight.unit.verbosename == '14 days')


def test_cal():
    assert(q.cal.unit.verbosename == 'thermochemical calorie')


def test_kcal():
    assert(q.kcal.unit.verbosename == 'thermochemical kilocalorie')


def test_cali():
    assert(q.cali.unit.verbosename == 'international calorie')


def test_kcali():
    assert(q.kcali.unit.verbosename == 'international kilocalorie')
