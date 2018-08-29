
PhysicalQuantity
================

Connects a value with a unit.


    >>> from PhysicalQuantities.quantity import PhysicalQuantity
    >>> g = PhysicalQuantity(9.81, 'm/s**2')


The value is stored in the attribute `.value`. It can acutally be any Python object,
however when working with units, especially converting between different unit scalings,
there can be multiplications with float values to take that into account.

For Numpy arrays, it is better to use `PhysicalQuantityArray` instead, as it subclasses
a `ndarray`.


Reference
---------

.. automodule:: PhysicalQuantities.quantity
   :members:
   :special-members:

