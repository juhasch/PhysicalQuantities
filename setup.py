from setuptools import find_packages, setup
from mypyc.build import mypycify

requirements = [
    'numpy',
    'IPython',
    'wrapt',
    'mypy'
    ]


setup(
    name="PhysicalQuantities",
    version="1.2.0",
    author="Juergen Hasch",
    author_email="juergen.hasch@elbonia.de",
    description="Allow calculations using physical quantities",
    license="BSD",
    keywords="Physical Quantities IPython",
    python_requires=">=3.11",
    url="https://github.com/juhasch/PhysicalQuantities",
    packages=find_packages(),
    ext_modules=mypycify([
        'PhysicalQuantities/fractdict.py'
    ]),
    install_requires=requirements,
    long_description_content_type='text/markdown',
    long_description="""
*PhysicalQuantities* is a Python module that allows calculations to be aware of physical units. Built-in unit
conversion ensures that calculations will result in the correct unit.

The main goals are:
 * easy use, especially conversion, scaling and interoperating with different units
 * focus on using units for engineering tasks
 * provide logarithmic dB calculations
 * allow seamless Numpy array operation

The module also contains an extension for IPython. This allows much simplified usage by typing in physical quantities
as number and unit:

    >>> a = 1m ; b = 1s
    >>> print("a=", a, ", b=",b,", a/b=", a/b)
    a= 1 m , b= 1 s , a/b= 1.0 m/s
    >>> u = 10V
    >>> u.dB
    >>> 20.0 dBV

""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
