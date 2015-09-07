# -*- coding: utf-8 -*-
import numpy as np
from .Quantity import *


def floor(q):
    """ Return the floor of the input, element-wise.
    :return: The floor of each element
    :rtype: PhysicalQuantity
    """
    value = np.floor(q.value)
    return q.__class__(value, q.unit)


def ceil(q):
    """ Return the ceiling of the input, element-wise.
    :return: The ceiling of each element
    :rtype: PhysicalQuantity
    """
    value = np.ceil(q.value)
    return q.__class__(value, q.unit)


def sqrt(q):
    """ Return the square root of the input, element-wise.
    :return: The floor of each element
    :rtype: PhysicalQuantity
    """
    value = np.sqrt(q.value)
    return q.__class__(value, q.unit)


def linspace(start, stop, num = 50,  endpoint=True, retstep=False):
    """ A units-enabled linspace
    :param start: start value
    :param stop:  stop value
    :param num: number of points
    :param endpoint: include stop point
    :param retstep: if true, return (samples, step)
    :return: return equally spaced samples between start and stop
    """
    if not isinstance(start, PhysicalQuantity) and not isinstance(stop, PhysicalQuantity):
        return np.linspace(start, stop, num,  endpoint, retstep)

    if isinstance(start, PhysicalQuantity) and isinstance(stop, PhysicalQuantity):
        if start.base.unit != stop.base.unit:
            raise UnitError("Cannot match units")

    unit = None
    if isinstance(start, PhysicalQuantity):
        start_value = start.value
        unit = start.unit
    else:
        start_value = start

    if isinstance(stop, PhysicalQuantity):
        stop_value = stop.value
        unit = stop.unit
    else:
        stop_value = stop

    array = np.linspace(start_value, stop_value, num,  endpoint, retstep)

    if retstep:
        return PhysicalQuantity(array[0], unit), PhysicalQuantity(array[1], unit)
    else:
        return array * PhysicalQuantity(1, unit)
