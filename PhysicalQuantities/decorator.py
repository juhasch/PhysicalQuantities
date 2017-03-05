"""Decorators to check units in parameters"""
import wrapt
from .Quantity import *
from .Unit import *


def checkbaseunit(arg, unit):
    """ Check if an argument is of a certain unit

    Parameters
    ----------
    arg: PhysicalQuantity
        argument with unit to be checked
    unit: str
        reference unit

    Returns
    -------
    bool
        True if argument has requested unit
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

    Parameters
    ----------
    arg: PhysicalQuantity
        Argument with unit to be checked
    unit: str
        Reference unit

    Returns
    -------
        Value without unit
    """
    if not isinstance(arg, PhysicalQuantity):
        return arg
    try:
        arg.to(unit)
        return arg.base.value
    except UnitError:
        raise UnitError('%s is not of unit %s' % (arg, unit))


def require_units(*units, **kunits):
    """ Decorator to check arguments of a function call

    Parameters
    ----------
    units: list
        list of units for arguments
**kwunits: list of keyword units for arguments

    Returns
    -------
        wrapper function

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
