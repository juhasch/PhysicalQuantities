
dB - Logarithmic Quantities
===========================

dB calculations can also be performed using the ``dBQuantity`` class:

.. code:: python

    >>> from PhysicalQuantities.dBQuantity import dBQuantity
    >>> a = dBQuantity(1, 'dBm')
    >>> a
    1 dBm


The IPython extension provides an easy way to do dB calculations:

.. code:: python

    >>> %load_ext PhysicalQuantities.ipython
    >>> p = 0 dBm
    >>> g = 20 dB
    >>> a = 10 dB
    >>> p + g - a
    10 dBm

The list of supported dBUnits is small:

.. code:: python

    >>> from PhysicalQuantities.dBQuantity import dB_unit_table
    >>> list(dB_unit_table.keys())
    ['dBnV',
     'dB',
     'dBV',
     'dBi',
     'dBnA',
     'dBuA',
     'dBc',
     'dBA',
     'dBW',
     'dBuV',
     'dBd',
     'dBm',
     'dBmA',
     'dBsm',
     'dBmV']


+-------+--------+-----------------+
| Name  | Unit   | Description     |
+=======+========+=================+
| dBnV  | V      |  dB Nanovolt    |
+-------+--------+-----------------+
| dBuV  | V      |  dB Microvolt   |
+-------+--------+-----------------+
| dBV   | V      |  dB Volt        |
+-------+--------+-----------------+
| dBnA  | A      |  dB Nanoampere  |
+-------+--------+-----------------+
| dBuA  | A      |  dB Microampere |
+-------+--------+-----------------+
| dBA   | A      |  dB Ampere      |
+-------+--------+-----------------+
| dBm   | W      |  dB Milliwatt   |
+-------+--------+-----------------+
| dBW   | W      |  dB Watt        |
+-------+--------+-----------------+
| dBsm  | m^2    |  dB Squaremeter |
+-------+--------+-----------------+

Converting to other units is easy:

.. code:: python

    >>> p = 0 dBm
    >>> print(p)
    0 dBm
    >>> print(p.dBW)
    -30.0 dBW
    >>> print(p.W)
    0.001 W


Absolute values (``dBm`` or ``dBW``) are handled differently compared to
unitless ``dB``:

.. code:: python

    >>> p = 0 dBW
    >>> p+p
    3.0102999566398121 dBW
    >>> g = 3 dB
    >>> p+g
    3 dBW


The ``_`` attribute to remove units is available too:

.. code:: python

    >>> p = 0 dBm
    >>> print(p.dBW)
    -30.0 dBW
    >>> print(p.dBW_)
    -30.0
    >>> print(p._)
    0


Internal representation
-----------------------

Calling the ``dBQuantity()`` constructor creates the desired object:

.. code:: python

    >>> a = dBQuantity(0.1,'dBm')
    >>> a
    0.1 dBm


The information is stored in two attributes:

.. code:: python

    >>> a.value, a.unitname
    (0.1, 'dBm')


The unit itself is represented as ``dBUnit`` object:

.. code:: python

    >>> u = a.unit
    >>> u
    <PhysicalQuantities.dBQuantity.dBUnit at 0x10baccf60>

The unit contains the name, the conversion factor (10 or 20), the
reference impedance and the underlying PhysicalUnit:

.. code:: python

    >>> u.name, u.factor, u.offset, u.z0, u.physicalunit
    ('dBm', 10, 0, 50 Ohm, <PhysicalUnit mW>)


For relative dB values, offset and physicalunit are unknown:

.. code:: python

    >>> a = 0dB
    >>> u = a.unit
    >>> u.name, u.factor, u.offset, u.z0, u.physicalunit
    ('dB', 0, 0, 50 Ohm, None)


Calling with ``islog=False`` converts the value considering the target unit to log:

.. code:: python

    >>> a = dBQuantity(0.1,'dBm', islog=False)
    >>> a
    -10.0 dBm

Conversion from and to dB
=========================

Most linear units can be converted to dB using the ``dB`` attribute:

.. code:: python

    >>> p = 1 mW
    >>> p.dB
    0.0 dBm
    >>> p = 10 dBm
    >>> p.lin
    10.0 mW


For relative dB values, the conversion factor has to be specified.
There are two helper functions to calculate :math:`10*log10(value)` or :math:`20*log10(value)`:

.. code:: python

    >>> from PhysicalQuantities.dBQuantity import dB10, dB20
    >>> dB10(10)
    10.0 dB
    >>> dB20(10)
    20.0 dB

Conversion back to linear values can be either :math:`10^{(value/10)}` or :math:`10^{(value/20)}`.
This can be simplified by using the properties ``lin10`` or ``lin20``:

.. code:: python

    >>> a = 10 dB
    >>> a.lin10
    10.0
    >>> a.lin20
    3.1622776601683795
