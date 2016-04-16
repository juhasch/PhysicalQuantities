# -*- coding: utf-8 -*-
import numpy as np
from .Quantity import *
from .Unit import UnitError
from . import isphysicalquantity, q

__all__ = ['floor', 'ceil', 'sqrt', 'linspace', 'tophysicalquantity']


def max(q):
    """Return the maximum of an array or maximum along an axis.

    Parameters
    ----------
    q : array_like
        Input data

    Returns
    -------
    array_like
        Maximum of an array or maximum along an axis
    """
    if isphysicalquantity(q):
        return q.__class__(np.max(q.value), q.unit)
    else:
        return np.max(q)

    
def floor(q):
    """ Return the floor of the input, element-wise.

    Parameters
    ----------
    q : array_like
        Input data

    Returns
    -------
    PhysicalQuantity
        The floor of each element

    Example
    -------
    >>> import PhysicalQuantities.numpywrapper as nw
    >>> nw.floor(1.3 mm)
    1 mm
    """
    if isphysicalquantity(q):
        return q.__class__(np.floor(q.value), q.unit)
    else:
        return np.floor(q)


def ceil(q):
    """ Return the ceiling of the input, element-wise.

    Parameters
    ----------
    q : array_like
        Input data

    Returns
    -------
    PhysicalQuantity
        The ceiling of each element

    Example
    -------
    >>> import PhysicalQuantities.numpywrapper as nw
    >>> nw.ceil(1.3 mm)
    2.0 mm
    """
    if isphysicalquantity(q):
        return q.__class__(np.ceil(q.value), q.unit)
    else:
        return np.ceil(q)


def sqrt(q):
    """ Return the square root of the input, element-wise.

    Parameters
    ----------
    q : array_like
        Input data

    Returns
    -------
    PhysicalQuantity
        The floor of each element

    Example
    -------
    >>> import PhysicalQuantities.numpywrapper as nw
    >>> nw.sqrt(4 m**2)
    2.0 m
    """
    if isphysicalquantity(q):
        value = np.sqrt(q.value)
        return q.__class__(value, q.unit**0.5)
    else:
        return np.sqrt(q)


def linspace(start, stop, num=50,  endpoint=True, retstep=False):
    """ A units-enabled linspace

    Parameters
    ----------
    start: PhysicalQuantity or float
        Start value
    stop:  PhysicalQuantity or float
        Stop value
    num: int
        Number of points
    endpoint: bool
        If true, include stop point
    retstep: bool
        If true, return (samples, step)

    Returns
    -------
        Return equally spaced samples between start and stop

    Example
    -------
    >>> import PhysicalQuantities.numpywrapper as nw
    >>> nw.linspace(0 GHz, 100 GHz, 200)
    """
    if not isinstance(start, PhysicalQuantity) and not isinstance(stop, PhysicalQuantity):
        return np.linspace(start, stop, num,  endpoint, retstep)

    if isinstance(start, PhysicalQuantity) and isinstance(stop, PhysicalQuantity):
        start.base.unit == stop.base.unit

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
        return PhysicalQuantity(array, unit)


def tophysicalquantity(arr, unit=None):
    """ Convert numpy array or list containing PhysicalQuantity elements to PhysicalQuantity object containing array or list

    Parameters
    -----------
    arr: array_like

    Returns
    -------
    PhysicalQuantity
        Array wrapped as PhysicalQuantity

    Example
    -------
    >>> a = [ 1mm, 2m, 3mm]
    >>> b = toPhysicalQuantity(a)
    >>> b
    [ 1 2000 3] mm
    """
    if isphysicalquantity(arr):
        if type(arr.value) is np.ndarray:
            # we are already a PQ array
            return arr
        if type(arr.value) is list:
            # convert list to array
            newarr = np.array(arr.value)
            return newarr * q[arr.unit]
        if type(arr.value) is not (list or np.array):
            # do nothing for single PQ values
            return arr
    else:
        if type(arr) is not (list or np.array):
            if unit is not None:
                # convert single values to PQ if unit is specified
                return arr * q[unit]
            else:
                raise UnitError('No unit given for value')

    for i, _a in enumerate(arr):
        if not isphysicalquantity(_a) and unit is None:
            raise UnitError('Element %d is not a physical quantity: %s' % (i,_a))

    if unit is None:
        unit = arr[0].unit
    if isphysicalquantity(arr[0]):
        valuetype = type(arr[0].value)
    else:
        valuetype = type(arr[0])

    newarr = np.zeros_like(arr, dtype=valuetype )
    for i, _a in enumerate(arr):
        if isphysicalquantity(_a):
            try:
                newarr[i] = _a.to(unit).value
            except UnitError:
                raise UnitError('Element %d is not same unit as others' % i)
        else:
            newarr[i] = _a
    return PhysicalQuantity(newarr, unit)


def argsort(array):
    """Returns the indices that would sort an array.
    Perform an indirect sort along the given axis using the algorithm specified by the kind keyword. It returns an array of indices of the same shape as a that index data along the given axis in sorted order.

    Parameters:	
    -----------
    a : array_like
        Array to sort.
    
    axis : int or None, optional
        Axis along which to sort. The default is -1 (the last axis). If None, the flattened array is used.
    
    kind : {‘quicksort’, ‘mergesort’, ‘heapsort’}, optional
        Sorting algorithm.
    
    order : str or list of str, optional
        When a is an array with fields defined, this argument specifies which fields to compare first, second, etc. A single field can be specified as a string, and not all fields need be specified, but unspecified fields will still be used, in the order in which they come up in the dtype, to break ties.
    
    Returns:
    --------
    index_array : ndarray, int
        Array of indices that sort a along the specified axis. In other words, a[index_array] yields a sorted a.

    """
    
    if isphysicalquantity(array):
        return np.argsort(array.value)
    else:
        return np.argsort(array)

def insert(array, obj, values):
    """Insert values along the given axis before the given indices.
    Parameters:	
    -----------
    arr : array_like
        Input array.
    
    obj : int, slice or sequence of ints
        Object that defines the index or indices before which values is inserted.
    
    values : array_like
        Values to insert into arr. If the type of values is different from that of arr, values is converted to the type of arr.
    
    axis : int, optional
        Axis along which to insert values. If axis is None then arr is flattened first.
    
    Returns:	
    --------
    out : ndarray
    
    A copy of arr with values inserted. Note that insert does not occur in-place: a new array is returned. If axis is None, out is a flattened array.

    """
    if isphysicalquantity(array):
        return np.insert(array.value, obj, values.value) * q[array.unit]
    else:
        return np.insert(array, obj, values)
