import os
import sys

from setuptools import setup

if sys.version_info < (3,6):
    sys.exit('Sorry, Python < 3.6 is not supported')


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="PhysicalQuantities",
    version="0.7.0",
    author="Juergen Hasch",
    author_email="juergen.hasch@elbonia.de",
    description="Allow calculations using physical quantities",
    license="BSD",
    keywords="Physical Quantities IPython",
    python_requires=">=3.6",
    url="http://packages.python.org/PhysicalQuantities",
    packages=['PhysicalQuantities'],
    install_requires=['numpy', 'IPython', 'wrapt'],
    long_description="""
PhysicalQuantities is a python module that allows calculations to be aware 
of physical units with a focus on engineering applications. 
Built-in unit conversion ensures that calculations will result in the correct aggregate unit.
""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
