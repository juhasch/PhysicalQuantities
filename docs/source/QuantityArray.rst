QuantityArray
=============

Subclasses a Numpy `ndarray` and adds a unit attribute. It can be used just like any Numpy
array.

Extra attributes
----------------

To create a `QuantityArray` use

    >>> from PhysicalQuantities.quantityarray import QuantityArray
    >>> qa = QuantityArray( <value>, <unit>)

Where `<value>` is an Numpy ndarray, and `<unit>' is a `PhysiclUnit` object or a string representing
a unit like `m` or `km/h`.

You can scale and remove units using attributes. If you have a variable `qa` of type
`QuantityArray` with unit `m`, you can rescale in `km` using `qa.km`. If you use `qa.km_` you
will get a `ndarray` view and the unit is stripped from the array.

Alternatively, more complicated units can be rescaled using the `.to()` function. So
`qa.to('km')` will scale the given units to km.

Examples
--------

.. code::

    >>> from PhysicalQuantities import QA
    >>> import numpy as np
    >>> a = np.random.randn(10)
    >>> b = QA(a, 'm/s')
    >>> b
    PhysicalQuantityArray([ 1.36836913  0.70860175  0.00633686 -0.54290276  0.82087296  0.49118831
      0.7917231   0.13107132  0.35147733  1.14482806], unit=m/s)
    >> b.view(np.ndarray)
    array([ 1.36836913  0.70860175  0.00633686 -0.54290276  0.82087296  0.49118831
      0.7917231   0.13107132  0.35147733  1.14482806])

    >>> b.to('mm/h')
    PhysicalQuantityArray([ 4926128.85358709  2550966.29803592    22812.69863759 -1954449.92312585
      2955142.65295286  1768277.90323167  2850203.14531766   471856.75616011
      1265318.38302892  4121381.00263216], unit=mm/h)
    >>> c = QA(a, 'km')
    >>> c.m
    PhysicalQuantityArray([1368.369126    708.60174945    6.33686073 -542.90275642  820.87295915
      491.18830645  791.72309592  131.07132116  351.47732862 1144.82805629], unit=m)
    >>> c.m_
    array([1368.369126  ,  708.60174945,    6.33686073, -542.90275642,
            820.87295915,  491.18830645,  791.72309592,  131.07132116,
            351.47732862, 1144.82805629])

Reference
---------

.. automodule:: PhysicalQuantities.quantityarray
   :members:
   :special-members:
