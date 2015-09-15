# -*- coding: utf-8 -*-

import wrapt
from .Quantity import *
from .Unit import *


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
        return True
    except UnitError:
        raise UnitError('%s is not of unit %s' % (arg, unit))


def dropunit(arg, unit):
    """ Drop unit of a given argument

    :param arg: argument with unit to be checked
    :param unit: reference unit
    :return: value without unit
    """
    if not isinstance(arg, PhysicalQuantity):
        return arg
    try:
        arg.unit.conversion_tuple_to(unit_table[unit])
        return arg.base.value
    except UnitError:
        raise UnitError('%s is not of unit %s' % (arg, unit))


def require_units(*units, **kunits):
    """ Decorator to check arguments of a function call

    :param *units: list of units for arguments
    :param **kwunits: list of keyword units for arguments

    >>> @require_units('V', 'A')
    >>> def power(u, i):
    >>>     return (u*i).W

    >>> @require_units(u='V', u='A')
    >>> def power(u, i):
    >>>     return (u*i).W

    """
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        for i, arg in enumerate(args):
            checkbaseunit(arg, units[i])
        for i, kwarg in enumerate(kwargs):
            checkbaseunit(kwarg, units[i])
        ret = wrapped(*args, **kwargs)
        return ret
    return wrapper


def optional_units(*units, **kunits):
    """ Decorator to check arguments of a function call

    :param units: list of units for arguments

    >>> @optional_units('V','A', return_unit='W')
    >>> def powero(u, i):
    >>>     return u*i

    >>> @optional_units(u='V', u='A', return_unit='W')
    >>> def power(u,i):
    >>>     return (u*i).W

    """
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        newargs = []
        for i, arg in enumerate(args):
            newargs.append(dropunit(arg, units[i]))
        newkwargs = {}
        for i, key in enumerate(kwargs):
            newkwargs[key] = dropunit(kwargs.get(key), kunits.get(key))
        return_value = wrapped(*newargs, **newkwargs)
        return_unit = kunits.get('return_unit','')
        if return_unit is not '':
            return_value = PhysicalQuantity(return_value, return_unit)
        return return_value
    return wrapper
