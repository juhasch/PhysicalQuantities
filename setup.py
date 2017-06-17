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
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
