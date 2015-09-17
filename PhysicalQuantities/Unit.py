# -*- coding: utf-8 -*-
""" PhysicalUnit class definition

Original author: Georg Brandl <georg@python.org>, https://bitbucket.org/birkenfeld/ipython-physics
"""

import numpy as np
import sys
import six
from .NDict import *


if sys.version_info > (2,):
    from functools import reduce


class UnitError(ValueError):
    pass


# Helper functions
def findunit(unit):
    """ Return PhysicalUnit class if given parameter is a valid unit

    :param unit: unit to check if valid
    :type unit: str
    :return: unit
    :rtype: PhysicalUnit
    """
    if isinstance(unit, six.string_types):
        name = str(unit).strip().replace('^', '**')
        if name[0:2] == '1/':
            name = '(' + name[2:] + ')**-1'
        try:
            unit = eval(name, unit_table)
        except NameError:
            raise UnitError('Invalid or unknown unit in %s' % name)
        for cruft in ['__builtins__', '__args__']:
            try:
                del unit_table[cruft]
            except KeyError:
                pass
    if not isphysicalunit(unit):
        raise UnitError('%s is not a unit' % str(unit))
    return unit


def convertvalue(value, src_unit, target_unit):
    """ Convert between units, if possible

    :param value: value in source units
    :param src_unit: source unit
    :type src_unit: PhysicalUnit
    :param target_unit: target unit
    :type target_unit: PhysicalUnit
    :return: value in target unit
    """
    (factor, offset) = src_unit.conversion_tuple_to(target_unit)
    if isinstance(value, list):
        raise UnitError('Cannot convert units for a list')
    return (value + offset) * factor


def isphysicalunit(x):
    """ Return true if valid PhysicalUnit class

    :param x: unit
    :type x: PhysicalUnit
    """
    return isinstance(x, PhysicalUnit)


class PhysicalUnit:
    """Physical unit.

    A physical unit is defined by a name (possibly composite), a scaling factor,
    and the exponentials of each of the SI base units that enter into it. Units
    can be multiplied, divided, and raised to integer powers.
    """

    def __init__(self, names, factor, powers, offset=0, url='', verbosename=''):
        """ Initialize unit object

        :param names: a dictionary mapping each name component to its
                      associated integer power (e.g. C{{'m': 1, 's': -1}})
                      for M{m/s}). As a shorthand, a string may be passed
                      which is assigned an implicit power 1.
        :type names: dict or str
        :param factor: a scaling factor
        :type factor: float
        :param powers: the integer powers for each of the nine base units
        :type powers: list
        :param offset: an additive offset to the base unit (used only for temperatures)
        :type offset: float
        :param url: URL describing the unit
        :type url: str
        :param verbosename: the verbose name of the unit (e.g. Coulomb)
        :type verbosename: str
        """

        self.prefixed = False
        self.baseunit = self
        self.verbosename = verbosename
        self.url = url
        if isinstance(names, six.string_types):
            self.names = NumberDict()
            self.names[names] = 1
        else:
            self.names = names
        self.factor = factor
        self.offset = offset
        self.powers = powers

    def set_name(self, name):
        self.names = NumberDict()
        self.names[name] = 1

    @property
    def name(self):
        """ Return name of unit

        :return: name of unit
        :rtype: str
        """
        num = ''
        denom = ''
        for unit in self.names.keys():
            power = self.names[unit]
            if power < 0:
                denom = denom + '/' + unit
                if power < -1:
                    denom = denom + '**' + str(-power)
            elif power > 0:
                num = num + '*' + unit
                if power > 1:
                    num = num + '**' + str(power)
        if len(num) == 0:
            num = '1'
        else:
            num = num[1:]
        return num + denom

    @property
    def _markdown_name(self):
        """ Return name of unit as markdown string

        :return: name of unit as markdown string
        :rtype: str
        """
        num = ''
        denom = ''
        for unit in self.names.keys():
            power = self.names[unit]
            if power < 0:
                if denom is '':
                    denom = '\\text{' + unit + '}'
                else:
                    denom = denom + '\\cdot \\text{' + unit + '}'
                if power < -1:
                    denom = denom + '^' + str(-power)
            elif power > 0:
                if num is '':
                    num = '\\text{' + unit + '}'
                else:
                    num = num + '\\cdot \\text{' + unit + '}'
                if power > 1:
                    num = num + '^{' + str(power) + '}'
        if num is '':
            num = '1'
        if denom is not '':
            name = '\\frac{' + num + '}{' + denom + '}'
        else:
            name = num
        name = name.replace('u', u'µ').replace('\\text{deg}', '\\,^{\\circ}').replace(' pi', ' \\pi ')
        return name

    @property
    def is_dimensionless(self):
        """ Check if no dimension is given

        :return: true if dimensionless
        :rtype: bool
        """
        return not reduce(lambda a, b: a or b, self.powers)

    @property
    def is_angle(self):
        """ Check if unit is an angle

        :return: true if unit is an angle
        :rtype: bool
        """
        return self.powers[7] == 1 and \
               reduce(lambda a, b: a + b, self.powers) == 1

    def __str__(self):
        """ Return string text representation of unit

        :return: Text representation of unit
        :rtype: str
        """
        name = self.name.strip().replace('**', u'^')
        return name

    def __repr__(self):
        return '<PhysicalUnit ' + self.name + '>'

    def _repr_markdown_(self):
        """ Return markdown representation for IPython notebook

        :return: Unit as LaTeX string
        :rtype: str
        """
        unit = self._markdown_name
        s = '$%s$' % unit
        return s

    def _repr_latex_(self):
        """ Return LaTeX representation for IPython notebook

        :return: Unit as LaTeX string
        :rtype: str
        """
        unit = self._markdown_name
        s = '%s' % unit
        return s

    @property
    def markdown(self):
        """ Return unit as a markdown formatted string

        :return: Unit as LaTeX string
        :rtype: str
        """
        return self._repr_markdown_()

    @property
    def latex(self):
        """ Return unit as a LaTeX formatted string

        :return: Unit as LaTeX string
        :rtype: str
        """
        return self._repr_latex_()

    def __gt__(self, other):
        """ Test if unit is greater than other unit

        :param other: other unit to compare with
        :type other: PhysicalUnit
        :return: true, if unit is greater than other unit
        :rtype: bool
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor > other.factor
        raise UnitError('Cannot compare different dimensions %s and %s' % (self, other))

    def __ge__(self, other):
        """ Test if unit is greater or equal than other unit

        :param other: other unit to compare with
        :type other: PhysicalUnit
        :return: true, if unit is greater or equal than other unit
        :rtype: bool
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor >= other.factor
        raise UnitError('Cannot compare different dimensions %s and %s' % (self, other))

    def __lt__(self, other):
        """ Test if unit is less than other unit

        :param other: other unit to compare with
        :type other: PhysicalUnit
        :return: true, if unit is less than other unit
        :rtype: bool
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor < other.factor
        raise UnitError('Cannot compare different dimensions %s and %s' % (self, other))

    def __le__(self, other):
        """ Test if unit is less or equal than other unit

        :param other: other unit to compare with
        :type other: PhysicalUnit
        :return: true, if unit is less or equal than other unit
        :rtype: bool
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor <= other.factor
        raise UnitError('Cannot compare different dimensions %s and %s' % (self, other))

    def __eq__(self, other):
        """ Test if unit is equal than other unit

        :param other: other unit to compare with
        :type other: PhysicalUnit
        :return: true, if unit is equal than other unit
        :rtype: bool
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor == other.factor
        raise UnitError('Cannot compare different dimensions %s and %s' % (self, other))

    def __mul__(self, other):
        """ Multiply two units

        :param other: other unit to multiply
        :type other: PhysicalUnit
        :return: multiplied unit
        :rtype: PhysicalUnit

        >>> from PhysicalQuantities import q
        >>> q.m.unit * q.s.unit
        m*s
        """
        if self.offset != 0 or (isphysicalunit(other) and other.offset != 0):
            raise UnitError('Cannot multiply units %s and %s with non-zero offset' % (self, other))
        if isphysicalunit(other):
            return PhysicalUnit(self.names + other.names,
                                self.factor * other.factor,
                                list(map(lambda a, b: a + b, self.powers, other.powers)))
        else:
            return PhysicalUnit(self.names + NumberDict({str(other): 1}),
                                self.factor*other, self.powers, self.offset)

    __rmul__ = __mul__

    def __div__(self, other):
        """ Divide two units

        :param other: other unit to divide
        :type other: PhysicalUnit
        :return: divided unit
        :rtype: PhysicalUnit

        >>> from PhysicalQuantities import q
        >>> q.m.unit / q.s.unit
        m/s
        """
        if self.offset != 0 or (isphysicalunit(other) and other.offset != 0):
            raise UnitError('Cannot divide units %s and %s with non-zero offset' % (self, other))
        if isphysicalunit(other):
            return PhysicalUnit(self.names - other.names,
                                self.factor / other.factor,
                                list(map(lambda a, b: a - b, self.powers, other.powers)))
        else:
            return PhysicalUnit(self.names + NumberDict({str(other): -1}),
                                self.factor/other, self.powers)

    def __rdiv__(self, other):
        if self.offset != 0 or (isphysicalunit(other) and other.offset != 0):
            raise UnitError('Cannot divide units %s and %s with non-zero offset' % (self,other))
        if isphysicalunit(other):
            return PhysicalUnit(other.names - self.names,
                                other.factor / self.factor,
                                list(map(lambda a, b: a - b, other.powers, self.powers)))
        else:
            return PhysicalUnit(NumberDict({str(other): 1}) - self.names,
                                other / self.factor,
                                list(map(lambda x: -x, self.powers)))

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __pow__(self, exponent):
        """ Power of a unit

        :param exponent: power exponent
        :type exponent: PhysicalUnit
        :return: unit to the power of exponent
        :rtype: PhysicalUnit

        >>> from PhysicalQuantities import q
        >>> q.m.unit ** 2
        m^2
        """
        if self.offset != 0:
            raise UnitError('Cannot exponentiate units %s and %s with non-zero offset' % (self, exponent))
        if isinstance(exponent, int):
            p = list(map(lambda x, p=exponent: x * p, self.powers))
            f = pow(self.factor, exponent)
            names = NumberDict((k, self.names[k] * exponent) for k in self.names)
            return PhysicalUnit(names, f, p)
        if isinstance(exponent, float):
            inv_exp = 1. / exponent
            rounded = int(np.floor(inv_exp + 0.5))
            if abs(inv_exp - rounded) < 1.e-10:
                if reduce(lambda a, b: a and b,
                          list(map(lambda x, e=rounded: x % e == 0, self.powers))):
                    f = pow(self.factor, exponent)
                    p = list(map(lambda x, p=rounded: x / p, self.powers))
                    p = [int(x) for x in p]
                    if reduce(lambda a, b: a and b,
                              list(map(lambda x, e=rounded: x % e == 0,
                                       self.names.values()))):
                        names = NumberDict((k, self.names[k] / rounded) for k in self.names)
                    else:
                        names = NumberDict()
                        if f != 1.:
                            names[str(f)] = 1
                        for i in range(len(p)):
                            names[base_names[i]] = p[i]
                    return PhysicalUnit(names, f, p)
                else:
                    raise UnitError('Illegal exponent %f' % exponent)
        raise UnitError('Only integer and inverse integer exponents allowed')

    def conversion_factor_to(self, other):
        """Return conversion factor to another unit

        :param other: other unit
        :type other: PhysicalUnit
        :return: float

        >>> from PhysicalQuantities import q
        >>> q.km.unit.conversion_factor_to(q.m.unit)
        1000.0
        """
        if self.powers != other.powers:
            raise UnitError('Incompatible units')
        if self.offset != other.offset and self.factor != other.factor:
            raise UnitError(('Unit conversion (%s to %s) cannot be expressed ' +
                             'as a simple multiplicative factor') %
                            (self.name, other.name))
        return self.factor / other.factor

    def conversion_tuple_to(self, other):
        """Return conversion factor and offset to another unit

        :param other: other unit
        :type other: PhysicalUnit
        :return: tuple (factor, offset)
        :rtype: float tuple

        >>> from PhysicalQuantities import q
        >>> q.km.unit.conversion_tuple_to(q.m.unit)
        (1000.0, 0.0)
        """
        if self.powers != other.powers:
            raise UnitError('Incompatible unit for conversion %s' % other.unit)

        # let (s1,d1) be the conversion tuple from 'self' to base units
        #   (ie. (x+d1)*s1 converts a value x from 'self' to base units,
        #   and (x/s1)-d1 converts x from base to 'self' units)
        # and (s2,d2) be the conversion tuple from 'other' to base units
        # then we want to compute the conversion tuple (S,D) from
        #   'self' to 'other' such that (x+D)*S converts x from 'self'
        #   units to 'other' units
        # the formula to convert x from 'self' to 'other' units via the
        #   base units is (by definition of the conversion tuples):
        #     ( ((x+d1)*s1) / s2 ) - d2
        #   = ( (x+d1) * s1/s2) - d2
        #   = ( (x+d1) * s1/s2 ) - (d2*s2/s1) * s1/s2
        #   = ( (x+d1) - (d1*s2/s1) ) * s1/s2
        #   = (x + d1 - d2*s2/s1) * s1/s2
        # thus, D = d1 - d2*s2/s1 and S = s1/s2
        factor = self.factor / other.factor
        offset = self.offset - (other.offset * other.factor / self.factor)
        return factor, offset


def _pretty(text):
    """ Pretty up unit name string

    :param text: input string
    :return: string with replaced characters
    """
    rep = {'**': '^', 'deg': '°', '*': '·', 'pi': 'π'}
    for k, v in rep.items():
        text = text.replace(k, v)
    return text


def units_html_list():
    """ List all defined units in a HTML table

    :return: list of all defined units
    :rtype: HTML string
    """
    from IPython.display import HTML
    table = "<table>"
    table += "<tr><th>Name</th><th>Base Unit</th><th>Quantity</th></tr>"
    for name in unit_table:
        unit = unit_table[name]
        if isinstance(unit, PhysicalUnit):
            if unit.prefixed is False:
                if isinstance(unit.baseunit, PhysicalUnit):
                    baseunit = '$ %s $' % unit.baseunit
                else:
                    baseunit = '$ %s $' % _pretty(unit.baseunit.name)
                table += "<tr><td>" + unit.name + '</td><td>' + baseunit + \
                         '</td><td><a href="' + unit.url + '" target="_blank">' + unit.verbosename + \
                         '</a></td></tr>'
    table += "</table>"
    return HTML(table)


def units_list():
    """ List all defined units

    :return: list of all defined units
    :rtype: str
    """
    units = []
    for name in unit_table:
        unit = unit_table[name]
        if isinstance(unit, PhysicalUnit) and unit.prefixed is False:
            units.append(unit.name)
    return units


def addunit(name, unit, verbosename='', prefixed=False, baseunit=None, url=''):
    """ Add new PhysicalUnit entry

     :param name: unit name
     :type name: str
     :param unit: unit
     :type unit: PhysicalUnit or str
     :param verbosename: a more verbose name for the unit
     :type verbosename: str
     :param prefixed: is this a prefixed unit
     :type prefixed: bool
     :param baseunit:
     :type baseunit: PhysicalUnit
     :param url: URL with information about unit
     :type url: str
    """
    if name in unit_table:
        raise KeyError('Unit ' + name + ' already defined')
    if isinstance(unit, str):
        newunit = eval(unit, unit_table)
        for cruft in ['__builtins__', '__args__']:
            try:
                del unit_table[cruft]
            except KeyError:
                pass
    else:
        newunit = unit
    newunit.set_name(name)
    newunit.verbosename = verbosename
    if prefixed is True:
        newunit.baseunit = baseunit
    else:
        newunit.baseunit = newunit
    newunit.prefixed = prefixed
    newunit.url = url
    unit_table[name] = newunit
    return name


def addprefixed(unitname, range='full'):
    """ Add prefixes to already defined unit

    :param unitname: name of unit to be prefixed, e.k. 'm' -> 'mm','cm','dm','km'
    :param range: 'engineering' -> 1e-18 to 1e12 or 'full' -> 1e-24 to 1e24
    """
    if range == 'engineering':
        _prefixes = _engineering_prefixes
    else:
        _prefixes = _full_prefixes
    unit = unit_table[unitname]
    for prefix in _prefixes:
        prefixedname = prefix[0] + unitname
        if prefixedname not in unit_table:
            addunit(prefixedname, prefix[1] * unit, prefixed=True, baseunit=unit, verbosename=unit.verbosename,
                    url=unit.url)


# add scaling prefixes
_full_prefixes = [
    ('Y', 1.e24), ('Z', 1.e21), ('E', 1.e18), ('P', 1.e15), ('T', 1.e12),
    ('G', 1.e9), ('M', 1.e6), ('k', 1.e3), ('h', 1.e2), ('da', 1.e1),
    ('d', 1.e-1), ('c', 1.e-2), ('m', 1.e-3), ('u', 1.e-6), ('n', 1.e-9),
    ('p', 1.e-12), ('f', 1.e-15), ('a', 1.e-18), ('z', 1.e-21),
    ('y', 1.e-24),
]

# actually, use a reduced set of scaling prefixes for engineering purposes:
_engineering_prefixes = [
    ('T', 1.e12),
    ('G', 1.e9), ('M', 1.e6), ('k', 1.e3),
    ('c', 1.e-2), ('m', 1.e-3), ('u', 1.e-6), ('n', 1.e-9),
    ('p', 1.e-12), ('f', 1.e-15), ('a', 1.e-18),
]

unit_table = {}
# These are predefined base units 
base_names = ['m', 'kg', 's', 'A', 'K', 'mol', 'cd', 'rad', 'sr']

addunit('kg', PhysicalUnit('kg', 1, [0, 1, 0, 0, 0, 0, 0, 0, 0]),
        url='https://en.wikipedia.org/wiki/Kilogram', verbosename='Kilogram')
addprefixed(addunit('g', PhysicalUnit('g', 0.001, [0, 1, 0, 0, 0, 0, 0, 0, 0]),
                    url='https://en.wikipedia.org/wiki/Kilogram', verbosename='Kilogram'), range='engineering')
addprefixed(addunit('s', PhysicalUnit('s', 1., [0, 0, 1, 0, 0, 0, 0, 0, 0]),
                    url='https://en.wikipedia.org/wiki/Second', verbosename='Second'), range='engineering')
addprefixed(addunit('A', PhysicalUnit('A', 1., [0, 0, 0, 1, 0, 0, 0, 0, 0]),
                    url='https://en.wikipedia.org/wiki/Ampere', verbosename='Ampere'), range='engineering')
addprefixed(addunit('K', PhysicalUnit('K', 1., [0, 0, 0, 0, 1, 0, 0, 0, 0]),
                    url='https://en.wikipedia.org/wiki/Kelvin', verbosename='Kelvin'), range='engineering')
addprefixed(addunit('mol', PhysicalUnit('mol', 1., [0, 0, 0, 0, 0, 1, 0, 0, 0]),
                    url='https://en.wikipedia.org/wiki/Mole_(unit)', verbosename='Mol'), range='engineering')
addprefixed(addunit('cd', PhysicalUnit('cd', 1., [0, 0, 0, 0, 0, 0, 1, 0, 0]),
                    url='https://en.wikipedia.org/wiki/Candela', verbosename='Candela'), range='engineering')
addprefixed(addunit('rad', PhysicalUnit('rad', 1., [0, 0, 0, 0, 0, 0, 0, 1, 0]),
                    url='https://en.wikipedia.org/wiki/Radian', verbosename='Radian'), range='engineering')
addprefixed(addunit('sr', PhysicalUnit('sr', 1., [0, 0, 0, 0, 0, 0, 0, 0, 1]),
                    url='https://en.wikipedia.org/wiki/Steradian', verbosename='Streradian'), range='engineering')
addprefixed(addunit('m', PhysicalUnit('m', 1., [1, 0, 0, 0, 0, 0, 0, 0, 0]),
                    url='https://en.wikipedia.org/wiki/Metre', verbosename='Metre'), range='engineering')
