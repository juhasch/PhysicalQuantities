import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="PhysicalQuantities",
    version="0.6.7",
    author="Juergen Hasch",
    author_email="juergen.hasch@elbonia.de",
    description="Allow calculations using physical quantities",
    license="BSD",
    keywords="Physical Quantities IPython",
    url="http://packages.python.org/PhysicalQuantities",
    packages=['PhysicalQuantities'],
    install_requires=['numpy', 'IPython', 'wrapt'],
    long_description=read('PhysicalQuantities is a python module that allows calculations to be aware of physical units'
                          'with a focus on engineering applications. Built-in unit conversion ensures that calculations'
                          'will result in the correct aggregate unit.'
                          'The module also contains an extension for IPython. This allows greatly simplified use by '
                          'typing in physical quantities directly as number and associated unit.'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
