"""Devine currencies

Due to the fluctuating exchange value, 

"""
import PhysicalQuantities

from .unit import add_composite_unit

add_composite_unit('Euro', 1., 'currency', verbosename='Euro',
                   url='https://en.wikipedia.org/wiki/Euro')

PhysicalQuantities.q.__init__()
