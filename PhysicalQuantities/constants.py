# Define additional physical constants

from math import pi

import numpy as np

from .quantity import *

c0 = PhysicalQuantity(299792458., 'm/s')
mu0 = PhysicalQuantity(4*np.pi*1e-7, 'N/A**2')
eps0 = PhysicalQuantity(8.854188e-12, 'F/m')
Grav = PhysicalQuantity(6.67384e-11, 'm**3/kg/s**2')
hpl = PhysicalQuantity(6.62606957e-34, 'J*s')
hbar = PhysicalQuantity(6.62606957e-34/(2*pi), 'J*s')
e0 = PhysicalQuantity(1.602176565e-19, 'C')
me = PhysicalQuantity(9.10938291e-31, 'kg')
mp = PhysicalQuantity(1.672621777e-27, 'kg')
mn = PhysicalQuantity(1.674927351e-27, 'kg')
NA = PhysicalQuantity(6.02214129e23, '1/mol')
kb = PhysicalQuantity(1.3806488e-23, 'J/K')
g0 = PhysicalQuantity(9.80665, 'm/s**2')
R = PhysicalQuantity(8.3144621, 'J/mol/K')
Ry = PhysicalQuantity(10973731.568539, '1/m')
mu_n = PhysicalQuantity(-0.96623647e-26, 'J/T')
gamma = PhysicalQuantity(183.247179, 'MHz/T')
sigmaT = PhysicalQuantity(6.652453e-29, 'm**2')
