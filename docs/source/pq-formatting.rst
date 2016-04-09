
Output Formatting in IPython
============================

Sometimes numerical calculation results don't look too pretty:

.. code:: python

    a = 7./3 m 
    a




.. math::

    2.3333333333333335 $\frac{1}{\text{m}}



IPython Magic
-------------

Using the IPython ``%precision`` magic, the displayed result can be made
prettier:

.. code:: python

    %precision 1
    a




.. math::

    2.3 $\frac{1}{\text{m}}



The magic also works for Numpy arrays:

.. code:: python

    b = np.array([1.234, 3.456])
    b




.. parsed-literal::

    array([ 1.2,  3.5])



The documentation for the ``%precision`` magic can be found here:
`link <http://ipython.org/ipython-doc/dev/api/generated/IPython.core.magics.basic.html#IPython.core.magics.basic.BasicMagics.precision>`__

Custom Formatting
-----------------

The ``%precision`` magic can be overridden individually for float
quantities, using the ``.format`` property of the ``PhysicalQuantity``
class. **Attention** The ``format`` property is taking Python
``formatter`` arguments.

.. code:: python

    a.format # default




.. parsed-literal::

    ''



.. code:: python

    a.format = '.3f'
    a




.. math::

    2.333 $\frac{1}{\text{m}}



Printing Output with Quantities
-------------------------------

.. code:: python

    a=1.23456 mm
    print(a)
    print("{:.3f}".format(a))
    print("%s" % a)
    print("%f" % a) # this returns base unit: m
    print("%.2f" % a.mm_)


.. parsed-literal::

    1.2 mm
    1.235 mm
    1.2 mm
    0.001235
    1.23
    

Another way to display quantities is using the ``Latex`` function.
Unfortunately, mixing math equations and Python's ``.format()`` needs a
little trick because of the ``{}``\ brackets.

.. code:: python

    from IPython.display import display, Math, Latex
    def disp(str):
        display(Latex(str))    
    v = 1.234567 m
    disp("$v_{min}$ is %s" %v)
    disp("$v_{min}$ is "+"{:.2f}".format(v))
    disp("$v_{min}$ is %s" % ("{:.2f}".format(v))) # Alternatively



.. math::

    v_{min}$ is 1.2 m



.. math::

    v_{min}$ is 1.23 m



.. math::

    v_{min}$ is 1.23 m


