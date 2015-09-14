
Autoscaling units
=================

Using the ``autoscale()`` method, quantities can be automatically
scaled:

.. code:: python

    a = 1e-3 m
    a.autoscale




1.0 :math:`\text{mm}`



.. code:: python

    a = 0.0003 s 
    a.autoscale




300.0 :math:`\text{µs}`



.. code:: python

    a = 1.0m
    a.autoscale




1.0 :math:`\text{m}`



.. code:: python

    %precision 2
    a = 3e-9 F
    a.autoscale




3.00 :math:`\text{nF}`



