
Autoscaling units
=================

Using the ``autoscale()`` method, quantities can be automatically
scaled:

.. code:: python

    a = 1e-3 m
    a.autoscale()




.. math::

    1.0 $mm



.. code:: python

    a = 0.0003 s 
    a.autoscale()




.. math::

    300.0 $\mu s



.. code:: python

    a = 1.0m
    a.autoscale()




.. math::

    1.0 $m


