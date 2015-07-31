# -*- coding: utf-8 -*-

import wrapt
from .Quantity import *


def checkbaseunit(arg, unit):
    """ Check if an argument is of a certain unit
    :param arg: argument with unit to be checked
    :param unit: reference unit
    :return: True if argument has requested unit
    """
    if not isinstance(arg, PhysicalQuantity):
        raise UnitError('%s is not a PhysicalQuantitiy' % arg)
    try:
        arg.unit.conversion_tuple_to(unit_table[unit])
    except UnitError:
        raise UnitError('%s is not of unit %s' % (arg, unit))


def require_units(*units):
    """ Decorator to check arguments of a function call
     TODO: kwargs
    :param units: list of units for arguments
    """
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        for i, arg in enumerate(args):
            checkbaseunit(arg, units[i])
        ret = wrapped(*args, **kwargs)
        return ret
    return wrapper


# Example:
#@require_units('V','A')
#def power(u,i):
#    return u*i
