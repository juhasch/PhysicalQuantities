
Sympy and PhysicalQuantities
============================

.. code:: python

    from sympy import *
    init_printing()

.. code:: python

    a = 1 m * Matrix([ [1,2,3], [4,5,6]])
    b = 1 cm * Matrix([ [1,2,3], [4,5,6]])

.. code:: python

    a




.. math::

    \left[\begin{matrix}1 & 2 & 3\\4 & 5 & 6\end{matrix}\right]$ $m



.. code:: python

    a+b




.. math::

    \left[\begin{matrix}1.01 & 2.02 & 3.03\\4.04 & 5.05 & 6.06\end{matrix}\right]$ $m



.. code:: python

    x = Symbol('x')

.. code:: python

    1 m * x




.. math::

    x$ $m



.. code:: python

    a = 2 m * x
    a




.. math::

    2 x$ $m



.. code:: python

    a/3




.. math::

    \frac{2 x}{3}$ $m



