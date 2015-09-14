
PhysicalQuantities - Basics
===========================

Installation
------------

The PhysicalQuantities module can be installed like any other Python
module: 1. Download package from
https://github.com/ipython-contrib/IPython-notebook-extensions/archive/master.zip
2. Unzpip 3. Install package using ``python setup.py install``

This document describes the basic use and some internals of the Python
module. If you are using IPython or the IPython notebook, you might want
to read the other example notebooks first.

Loading the Python Module
-------------------------

.. code:: python

    import PhysicalQuantities as pq

You can now define physical quantities using the
``PhysicalQuantity(value, unit)`` constructor:

.. code:: python

    g = pq.PhysicalQuantity(1.1, 'm')

or as the shortcut ``Q()``:

.. code:: python

    g = pq.Q(1.1, 'm')

This creates a new ``PhysicalQuantity`` object:

.. code:: python

    print("object: %s" % g)
    print("object type : %s" % type(g))


.. parsed-literal::

    object: 1.1 m
    object type : <class 'PhysicalQuantities.Quantity.PhysicalQuantity'>


The value and unit are stored as attributes of the class:

.. code:: python

    print("value: %s" % g.value)
    print("value type: %s" % type(g.value))
    print("unit: %s" % g.unit)
    print("unit type: %s" % type(g.unit))


.. parsed-literal::

    value: 1.1
    value type: <class 'float'>
    unit: m
    unit type: <class 'PhysicalQuantities.Unit.PhysicalUnit'>


Using ``.to()`` let's you convert to other representations of the unit.
This can be used for scaling or to express the quantity in a derived
unit. The ``.base`` property will convert

.. code:: python

    g = pq.PhysicalQuantity(1.1, 'm')
    print("g = %s" % g)
    print("g in mm = %s" %g.to('mm'))
    x = pq.PhysicalQuantity(2, 'm*kg/s**2')
    print("x = %s" %x)
    print("x in N = %s" % x.to('N'))
    u = 1 V
    print("u = %s" %u)
    print("u in base units = %s" %u.base)


.. parsed-literal::

    g = 1.1 m
    g in mm = 1100.0 mm
    x = 2 kg*m/s^2
    x in N = 2.0 N
    u = 1 V
    u in base units = 1.0 kg*m^2/A/s^3


Scaling of simple units is easy using scaling attributes:

.. code:: python

    print(g.nm)
    print(g.um)
    print(g.mm)
    print(g.cm)
    print(g.m)
    print(g.km)


.. parsed-literal::

    1100000000.0 nm
    1100000.0 um
    1100.0 mm
    110.00000000000001 cm
    1.1 m
    0.0011 km


The physical quantity can converted back to a unitless value using the
underscore ``_`` with the scaling attribute:

.. code:: python

    print(g.nm_)
    print(g.um_)
    print(g.mm_)
    print(g.cm_)
    print(g.m_)
    print(g.km_)


.. parsed-literal::

    1100000000.0
    1100000.0
    1100.0
    110.00000000000001
    1.1
    0.0011


Internal Representation
-----------------------

Internally, a physical quantity is represented using two classes: \*
``PhysicalQuantity`` holding the value and the unit \* ``PhysicalUnit``
describing the unit

.. code:: python

    a = pq.Q([1,2,3], 'm**2*s**3/A**2/kg')
    a.value




.. parsed-literal::

    [1, 2, 3]



The ``value`` attribute is basically only a container, allowing
different types of values. Tested types are: \* integers \* floats \*
complex numbers \* uncertainties \* numpy arrays \* lists

.. code:: python

    a.unit




:math:`\frac{\text{m}^{2}\cdot \text{s}^{3}}{\text{A}^2\cdot \text{kg}}`



.. code:: python

    type(a.unit)




.. parsed-literal::

    PhysicalQuantities.Unit.PhysicalUnit



The unit is stored in a ``PhysicalUnit`` class. This class has a number
of attributes: \* ``factor`` - scaling factor from base units \*
``powers`` - list of base units contained in unit \* ``prefixed`` - unit
is a scaled version of a base unit

.. code:: python

    pq.Q(1,'mm').unit.factor, pq.Q(1,'mm').unit.prefixed




.. parsed-literal::

    (0.001, True)



.. code:: python

    print(pq.base_names) # list of base units
    print(a.unit.powers)
    print(a.unit)


.. parsed-literal::

    ['m', 'kg', 's', 'A', 'K', 'mol', 'cd', 'rad', 'sr']
    [2, -1, 3, -2, 0, 0, 0, 0, 0]
    m^2*s^3/A^2/kg


