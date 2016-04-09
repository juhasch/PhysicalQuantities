
Back to `Index <Index.ipynb>`__

Using PhysicalQuantities in IPython
===================================

The IPython extension makes using physical quantities easier. To load
the extension use:

.. code:: python

    %load_ext PhysicalQuantities.ipython


.. parsed-literal::

    The PhysicalQuantities.ipython extension is already loaded. To reload it, use:
      %reload_ext PhysicalQuantities.ipython
    

Now entering a physical quantities gets very easy:

.. code:: python

    d = 2.3 s**3
    t = 3 A
    v = 2.3e3 * d / t

.. code:: python

    print("d = %s" %d)
    print("t = %s" %t)
    print("v = %s" %v)


.. parsed-literal::

    d = 2.3 s^3
    t = 3 A
    v = 1763.3333333333333 s^3/A
    

Unit conversion
---------------

The easiest way to scale a unit is to use prefix attributes:

.. code:: python

    u = 1 V
    print(u)
    print(u.mV)
    print(u.uV)


.. parsed-literal::

    1 V
    1000.0 mV
    1000000.0 uV
    

To convert between different representations of a unit, ``to()`` can be
used:

.. code:: python

    a = 1 N * 1 m
    print(a)
    print(a.to('J'))


.. parsed-literal::

    1 N*m
    1.0 J
    

Using other value types
-----------------------

The ``PhysicalQuantity`` class tries to be a wrapper around the value of
a given quantity, i.e. not only single numbers can be used. For examples
using Numpy arrays, take a look at the `Using Numpy
Arrays <pq-numpy.ipynb>`__ notebook.

.. code:: python

    u = (1 + 1j) * 1V
    print("u = %s" %u)
    u = [1,2,3] * 1V
    print("u = %s" %u)


.. parsed-literal::

    u = (1+1j) V
    u = [1, 2, 3] V
    

List of all defined Units:
--------------------------

All predefined units can be listed using the ``list()`` or
``html_list()`` function of a unit:

**BUG:** Links for base units are missing

.. code:: python

    import PhysicalQuantities as pq
    pq.units_html_list()




.. raw:: html

    <table><tr><th>Name</th><th>Base Unit</th><th>Quantity</th></tr><tr><td>arcsec</td><td>$ arcsec $</td><td><a href="" target="_blank">seconds of arc</a></td></tr><tr><td>arcmin</td><td>$ arcmin $</td><td><a href="" target="_blank">minutes of arc</a></td></tr><tr><td>J</td><td>$ J $</td><td><a href="https://en.wikipedia.org/wiki/Joule" target="_blank">Joule</a></td></tr><tr><td>Pa</td><td>$ Pa $</td><td><a href="https://en.wikipedia.org/wiki/Pascal_(unit)" target="_blank">Pascal</a></td></tr><tr><td>lx</td><td>$ lx $</td><td><a href="https://en.wikipedia.org/wiki/Lux" target="_blank">Lux</a></td></tr><tr><td>Hz</td><td>$ Hz $</td><td><a href="https://en.wikipedia.org/wiki/Hertz" target="_blank">Hertz</a></td></tr><tr><td>C</td><td>$ C $</td><td><a href="https://en.wikipedia.org/wiki/Coulomb" target="_blank">Coulomb</a></td></tr><tr><td>T</td><td>$ T $</td><td><a href="https://en.wikipedia.org/wiki/Tesla_(unit)" target="_blank">Tesla</a></td></tr><tr><td>deg</td><td>$ deg $</td><td><a href="http://en.wikipedia.org/wiki/Degree_%28angle%29" target="_blank">Degree</a></td></tr><tr><td>h</td><td>$ h $</td><td><a href="https://en.wikipedia.org/wiki/Hour" target="_blank">Hour</a></td></tr><tr><td>N</td><td>$ N $</td><td><a href="https://en.wikipedia.org/wiki/Newton_(unit)" target="_blank">Newton</a></td></tr><tr><td>S</td><td>$ S $</td><td><a href="https://en.wikipedia.org/wiki/Siemens_(unit)" target="_blank">Siemens</a></td></tr><tr><td>sr</td><td>$ sr $</td><td><a href="https://en.wikipedia.org/wiki/Steradian" target="_blank">Streradian</a></td></tr><tr><td>g</td><td>$ g $</td><td><a href="https://en.wikipedia.org/wiki/Kilogram" target="_blank">Kilogram</a></td></tr><tr><td>mol</td><td>$ mol $</td><td><a href="https://en.wikipedia.org/wiki/Mole_(unit)" target="_blank">Mol</a></td></tr><tr><td>lm</td><td>$ lm $</td><td><a href="https://en.wikipedia.org/wiki/Lumen_(unit)" target="_blank">Lumen</a></td></tr><tr><td>W</td><td>$ W $</td><td><a href="https://en.wikipedia.org/wiki/Watt" target="_blank">Watt</a></td></tr><tr><td>rad</td><td>$ rad $</td><td><a href="https://en.wikipedia.org/wiki/Radian" target="_blank">Radian</a></td></tr><tr><td>m</td><td>$ m $</td><td><a href="https://en.wikipedia.org/wiki/Metre" target="_blank">Metre</a></td></tr><tr><td>Ohm</td><td>$ Ohm $</td><td><a href="https://en.wikipedia.org/wiki/Ohm_(unit)" target="_blank">Ohm</a></td></tr><tr><td>Wb</td><td>$ Wb $</td><td><a href="https://en.wikipedia.org/wiki/Weber_(unit)" target="_blank">Weber</a></td></tr><tr><td>H</td><td>$ H $</td><td><a href="https://en.wikipedia.org/wiki/Henry_(unit)" target="_blank">Henry</a></td></tr><tr><td>A</td><td>$ A $</td><td><a href="https://en.wikipedia.org/wiki/Ampere" target="_blank">Ampere</a></td></tr><tr><td>cd</td><td>$ cd $</td><td><a href="https://en.wikipedia.org/wiki/Candela" target="_blank">Candela</a></td></tr><tr><td>F</td><td>$ F $</td><td><a href="https://en.wikipedia.org/wiki/Farad" target="_blank">Farad</a></td></tr><tr><td>kg</td><td>$ kg $</td><td><a href="https://en.wikipedia.org/wiki/Kilogram" target="_blank">Kilogram</a></td></tr><tr><td>K</td><td>$ K $</td><td><a href="https://en.wikipedia.org/wiki/Kelvin" target="_blank">Kelvin</a></td></tr><tr><td>V</td><td>$ V $</td><td><a href="https://en.wikipedia.org/wiki/Volt" target="_blank">Volt</a></td></tr><tr><td>min</td><td>$ min $</td><td><a href="https://en.wikipedia.org/wiki/Hour" target="_blank">Minute</a></td></tr><tr><td>s</td><td>$ s $</td><td><a href="https://en.wikipedia.org/wiki/Second" target="_blank">Second</a></td></tr></table>



