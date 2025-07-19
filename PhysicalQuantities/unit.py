""" PhysicalUnit class definition

Original author: Georg Brandl <georg@python.org>, https://bitbucket.org/birkenfeld/ipython-physics
"""
from __future__ import annotations
import copy
import json
from functools import reduce, lru_cache
from typing import Dict
from fractions import Fraction

import numpy as np

from .fractdict import FractionalDict
# Remove top-level import causing circular dependency
# from .quantity import PhysicalQuantity


class UnitError(ValueError):
    pass


class PhysicalUnit:
    prefixed: bool = False
    """Physical unit.

    A physical unit is defined by a name (possibly composite), a scaling factor, and the exponentials of each of
    the SI base units that enter into it. Units can be multiplied, divided, and raised to integer powers.

    Attributes
    ----------
    prefixed: bool
        If instance is a scaled version of a unit
    baseunit: PhysicalUnit
        Base unit if prefixed, otherwise self
    names: FractionalDict
        A dictionary mapping each name component to its associated integer power (e.g. `{'m': 1, 's': -1}`).
    factor: float
        A scaling factor from base units
    powers: list[int]
        The integer powers for each of the nine base units:
        ['m', 'kg', 's', 'A', 'K', 'mol', 'cd', 'rad', 'sr']
    offset: float
        An additive offset to the unit (used only for temperatures)
    url: str
        URL describing the unit
    verbosename: str
        The verbose name of the unit (e.g. Coulomb)
    unece_code: str
        Official unit code
        (see https://www.unece.org/fileadmin/DAM/cefact/recommendations/rec20/rec20_Rev9e_2014.xls)

    """

    def __init__(self, names, factor: float, powers: list[int], offset: float = 0, url: str = '', verbosename: str = '',
                 unece_code: str = ''):
        """ Initialize object

        Parameters
        ----------
        names: FractionalDict | str
            A dictionary mapping each name component to its associated integer power (e.g. `{'m': 1, 's': -1}`).
            As a shorthand, a string may be passed which is assigned an implicit power 1.
        factor: float
            A scaling factor from base units
        powers: list[int]
            The integer powers for each of the nine base units:
            ['m', 'kg', 's', 'A', 'K', 'mol', 'cd', 'rad', 'sr']
        offset: float, optional
            An additive offset to the unit (used only for temperatures). Default is 0.
        url: str, optional
            URL describing the unit. Default is ''.
        verbosename: str, optional
            The verbose name of the unit (e.g. Coulomb). Default is ''.
        unece_code: str, optional
            Official unit code
            (see https://www.unece.org/fileadmin/DAM/cefact/recommendations/rec20/rec20_Rev9e_2014.xls).
            Default is ''.

        """
        self.baseunit = self
        self.verbosename = verbosename
        self.url = url
        if isinstance(names, str):
            self.names = FractionalDict()
            self.names[names] = 1
        else:
            self.names = FractionalDict()
            for _name in names:
                self.names[_name] = names[_name]
        self.factor = factor
        self.offset = offset
        if len(base_names) != len(powers):
            raise ValueError('Invalid number of powers given for existing base_names')
        self.powers = powers
        self.unece_code = unece_code

    def set_name(self, name):
        """Set unit name as FractionalDict

        Parameters
        ----------
        name: str
            Unit name
        """
        self.names = FractionalDict()
        self.names[name] = 1

    @property
    def name(self) -> str:
        """ Return name of unit

        Returns
        -------
        str
            Name of unit (e.g., 'm/s', 'kg*m^2/s^2').
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
    def _markdown_name(self) -> str:
        """ Return name of unit as markdown string

        Returns
        -------
        str
            Name of unit formatted as a markdown/LaTeX math string.
        """
        num = ''
        denom = ''
        for unit in self.names.keys():
            power = self.names[unit]
            if power < 0:
                if denom == '':
                    denom = '\\text{' + unit + '}'
                else:
                    denom = denom + '\\cdot \\text{' + unit + '}'
                if power < -1:
                    denom = denom + '^' + str(-power)
            elif power > 0:
                if num == '':
                    num = '\\text{' + unit + '}'
                else:
                    num = num + '\\cdot \\text{' + unit + '}'
                if power > 1:
                    num = num + '^{' + str(power) + '}'
        if num == '':
            num = '1'
        if denom != '':
            name = '\\frac{' + num + '}{' + denom + '}'
        else:
            name = num
        name = name.replace('\\text{deg}', '\\,^{\\circ}').replace(' pi', ' \\pi ')
        return name

    @property
    def is_power(self) -> bool:
        """ Test if unit is a power unit (or related, like energy or area for dBsm).

        Used for dB conversion logic.
        TODO: This detection logic is currently very basic.

        Returns
        -------
        bool
            True if it is considered a power unit (e.g., W, J, m^2), False otherwise.
        """
        p = self.powers
        # Indices: 0:m, 1:kg, 2:s, 3:A, 4:K, 5:mol, 6:cd, 7:rad, 8:sr
        # Check for Area (L^2), e.g., m^2 for dBsm
        if p[0] == 2 and sum(abs(x) for x in p) == 2:
            return True
        # Check for Energy (M L^2 T^-2) or Power (M L^2 T^-3) dimensions
        # Original check used p[3] > -1 (Ampere), likely a typo.
        # Matching comment: (L^2 M T^-n, n>=2)
        # Refined check: Ensure Ampere dimension (p[3]) is 0 for true power/energy units.
        if p[0] == 2 and p[1] == 1 and p[2] <= -2 and p[3] == 0:
            return True
        return False

    @property
    def is_dimensionless(self) -> bool:
        """ Check if no dimension is given

        Returns
        -------
        bool
            True if dimensionless, False otherwise.
        """
        # Check if all power exponents are zero
        return not any(self.powers)

    @property
    def is_angle(self) -> bool:
        """ Check if unit is an angle

        Returns
        -------
        bool
            True if unit is an angle, False otherwise.
        """
        # Check if radian power is 1 and all other powers sum to 1 (meaning only radian is non-zero)
        return self.powers[7] == 1 and sum(self.powers) == 1

    def __str__(self) -> str:
        """ Return string text representation of unit

        Returns
        -------
        str
            Text representation of unit (e.g., 'm/s', 'km/h^2').
        """
        name = self.name.strip().replace('**', '^')
        return name

    def __repr__(self) -> str:
        """Return unambiguous string representation of the unit."""
        return f'<PhysicalUnit {self.name}>'

    def _repr_markdown_(self) -> str:
        """ Return markdown representation for IPython notebooks.

        Returns
        -------
        str
            Unit formatted as a markdown math string (e.g., '$\\frac{\\text{m}}{\\text{s}}$').
        """
        unit = self._markdown_name
        s = '$%s$' % unit
        return s

    def _repr_latex_(self) -> str:
        """ Return LaTeX representation for IPython notebooks.

        Returns
        -------
        str
            Unit formatted as a raw LaTeX math string (e.g., '\\frac{\\text{m}}{\\text{s}}').
        """
        unit = self._markdown_name
        s = '%s' % unit
        return s

    @property
    def markdown(self) -> str:
        """ Return unit as a markdown formatted string.

        Returns
        -------
        str
            Unit formatted as a markdown math string (e.g., '$\\frac{\\text{m}}{\\text{s}}$').
        """
        return self._repr_markdown_()

    @property
    def latex(self) -> str:
        """ Return unit as a LaTeX formatted string.

        Returns
        -------
        str
            Unit formatted as a raw LaTeX math string (e.g., '\\frac{\\text{m}}{\\text{s}}').
        """
        return self._repr_latex_()

    def __gt__(self, other) -> bool:
        """ Test if unit is greater than other unit

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to compare with

        Returns
        -------
        bool
            True, if unit is greater than other unit
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor > other.factor
        raise UnitError(f'Cannot compare different dimensions {self} and {other}')

    def __ge__(self, other) -> bool:
        """ Test if unit is greater or equal than other unit

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to compare with

        Returns
        -------
        bool
            True, if unit is greater or equal than other unit
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor >= other.factor
        raise UnitError(f'Cannot compare different dimensions {self} and {other}')

    def __lt__(self, other) -> bool:
        """ Test if unit is less than other unit

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to compare with

        Returns
        -------
        bool
            True, if unit is less than other unit
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor < other.factor
        raise UnitError(f'Cannot compare different dimensions {self} and {other}')

    def __le__(self, other) -> bool:
        """ Test if unit is less or equal than other unit

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to compare with

        Returns
        -------
        bool
            True, if unit is less or equal than other unit
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor <= other.factor
        raise UnitError(f'Cannot compare different dimensions {self} and {other}')

    def __eq__(self, other) -> bool:
        """ Test if unit is equal than other unit

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to compare with

        Returns
        -------
        bool
            True, if unit is equal than other unit
        """
        if isphysicalunit(other):
             # Check for compatible dimensions first
             if self.powers != other.powers:
                 # Units with different dimensions cannot be equal
                 return False
             # Consider using tolerance for float comparison if needed, e.g., math.isclose
             return self.factor == other.factor and self.offset == other.offset
         # If other is not a PhysicalUnit, they are not equal
        return False

    def __mul__(self, other):
        """ Multiply units with other value

        Parameters
        ----------
        other: PhysicalUnit | PhysicalQuantity | number
            Value or unit to multiply with

        Returns
        -------
        PhysicalUnit or PhysicalQuantity
            Resulting unit or quantity

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.m.unit * q.s.unit
        <PhysicalUnit m*s>
        >>> q.m.unit * 5
        <PhysicalQuantity 5 m>
        >>> 5 * q.m.unit
        <PhysicalQuantity 5 m>
        """
        # Import locally
        from .quantity import PhysicalQuantity

        if self.offset != 0:
            raise UnitError(f'Cannot multiply unit {self} with non-zero offset')

        if isphysicalunit(other):
            if other.offset != 0:
                raise UnitError(f'Cannot multiply unit {other} with non-zero offset')
            return PhysicalUnit(self.names + other.names,
                                self.factor * other.factor,
                                list(map(lambda a, b: a + b, self.powers, other.powers)))
        elif isinstance(other, PhysicalQuantity):
            # Defer to PhysicalQuantity's __rmul__ for unit * quantity
            # This ensures the result is a PhysicalQuantity with combined unit and scaled value
            # Let standard dispatch handle calling PhysicalQuantity.__mul__ or __rmul__
            return other * self
        else:
            # Assume 'other' is a scalar: scalar * unit
            try:
                # Check if 'other' can be treated as a number
                float(other)
                # Return PhysicalQuantity(scalar, unit)
                return PhysicalQuantity(other, self)
            except (ValueError, TypeError):
                raise TypeError(f"Unsupported operand type(s) for *: '{type(self).__name__}' and '{type(other).__name__}'")

    # __rmul__ should handle scalar * unit correctly by calling __mul__
    # No change needed here if __mul__ handles scalar * unit correctly
    __rmul__ = __mul__

    def __truediv__(self, other):
        """ Divide unit by another value (true division).

        Parameters
        ----------
        other: PhysicalUnit | PhysicalQuantity | number
            Value or unit to divide by

        Returns
        -------
        PhysicalUnit or PhysicalQuantity
            Resulting unit or quantity

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.m.unit / q.s.unit
        <PhysicalUnit m/s>
        >>> q.m.unit / 5
        <PhysicalQuantity 0.2 m>
        """
        from .quantity import PhysicalQuantity # Import locally
        if self.offset != 0:
             raise UnitError(f'Cannot divide unit {self} with non-zero offset in numerator')

        if isphysicalunit(other):
            if other.offset != 0:
                raise UnitError(f'Cannot divide unit {other} with non-zero offset in denominator')
            return PhysicalUnit(self.names - other.names,
                                self.factor / other.factor,
                                list(map(lambda a, b: a - b, self.powers, other.powers)))
        elif isinstance(other, PhysicalQuantity):
            # Let PhysicalQuantity handle division: quantity**-1 * self
            return (other ** -1) * self
        else:
            # Assume 'other' is a scalar divisor
            try:
                scalar_denominator = float(other)
                if scalar_denominator == 0:
                    raise ZeroDivisionError("Scalar division by zero")
                return PhysicalQuantity(1.0 / scalar_denominator, self)
            except (ValueError, TypeError):
                raise TypeError(f"Unsupported operand type(s) for /: '{type(self).__name__}' and '{type(other).__name__}'")


    def __rtruediv__(self, other):
        """ Called for `other / self` (true division).

        Handles `scalar / unit`.

        Parameters
        ----------
        other: number
            Scalar numerator

        Returns
        -------
        PhysicalUnit
            Resulting reciprocal unit, scaled by the scalar.

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> 10 / q.s.unit
        <PhysicalUnit 10/s>
        """
        if self.offset != 0:
            raise UnitError(f'Cannot divide unit {self} with non-zero offset in denominator')

        # Note: unit / unit is handled by __truediv__
        # This method primarily handles scalar / unit
        try:
            scalar_numerator = float(other)
            # Calculate new factor for the reciprocal unit, scaled by the numerator
            # Avoid division by zero for factor
            if self.factor == 0:
                raise ZeroDivisionError("Division by unit with zero factor")
            new_factor = scalar_numerator / self.factor
            # Invert powers and names for the resulting unit
            new_powers = [-p for p in self.powers]
            new_names = FractionalDict({name: -power for name, power in self.names.items()})
            # Create and return the new reciprocal PhysicalUnit
            return PhysicalUnit(new_names, new_factor, new_powers)
        except (ValueError, TypeError):
             raise TypeError(f"Unsupported operand type(s) for /: '{type(other).__name__}' and '{type(self).__name__}'")

    def __floordiv__(self, other):
        """ Divide unit by another value (floor division).

        Note: Floor division is primarily meaningful for the scalar value
        when dividing by a scalar. For unit/unit or unit/quantity,
        it behaves like true division for the unit part, but the resulting
        scalar factor might not be intuitive or physically standard.

        Parameters
        ----------
        other: PhysicalUnit | PhysicalQuantity | number
            Value or unit to divide by

        Returns
        -------
        PhysicalUnit or PhysicalQuantity
            Resulting unit or quantity

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.km.unit // q.m.unit # Operates on factors, returns unit
        <PhysicalUnit km/m>
        >>> q.m.unit // 5
        <PhysicalQuantity 0.0 m>
        """
        from .quantity import PhysicalQuantity # Import locally
        if self.offset != 0:
             raise UnitError(f'Cannot divide unit {self} with non-zero offset in numerator')

        if isphysicalunit(other):
             if other.offset != 0:
                raise UnitError(f'Cannot divide unit {other} with non-zero offset in denominator')
             # Floor division applies to the factor
             new_factor = self.factor // other.factor
             return PhysicalUnit(self.names - other.names,
                                 new_factor,
                                 list(map(lambda a, b: a - b, self.powers, other.powers)))
        elif isinstance(other, PhysicalQuantity):
             # This case is potentially ambiguous. What does unit // quantity mean?
             # Let's define it as floor division of the scalar part resulting from (1/quantity) * unit
             # (1/other) * self -> calculate value and apply floor
             temp_quantity = (other ** -1) * self
             # We need the value part for floor division. Assuming PhysicalQuantity has a 'value' attribute
             # This requires knowing the structure of PhysicalQuantity
             # If PhysicalQuantity doesn't directly support floor division in this way,
             # this operation might need further definition or restriction.
             # For now, let's raise an error as the semantics are unclear.
             raise TypeError(f"Floor division between PhysicalUnit and PhysicalQuantity is not clearly defined.")

        else:
            # Assume 'other' is a scalar divisor
            try:
                scalar_denominator = float(other)
                if scalar_denominator == 0:
                     raise ZeroDivisionError("Scalar division by zero")
                # Perform floor division on the resulting scalar value
                return PhysicalQuantity(1.0 // scalar_denominator, self)
            except (ValueError, TypeError):
                raise TypeError(f"Unsupported operand type(s) for //: '{type(self).__name__}' and '{type(other).__name__}'")

    # __rfloordiv__ for scalar // unit could be added if needed,
    # but its physical meaning is often obscure.

    # Keep __div__ and __rdiv__ assignments for Python 2 compatibility if needed,
    # but __truediv__ and __rtruediv__ are preferred in Python 3.
    # If strictly Python 3+, these aliases can be removed.
    __div__ = __truediv__
    __rdiv__ = __rtruediv__

    def __pow__(self, exponent: int | float):
        """ Power of a unit

        Parameters
        ----------
        exponent: int | float
            Power exponent (Must be integer or inverse of integer)

        Returns
        -------
        PhysicalUnit
            Unit to the power of exponent

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.m.unit ** 2
        m^2
        """
        if self.offset != 0:
            raise UnitError('Cannot exponentiate units %s and %s with non-zero offset' % (self, exponent))
        if isinstance(exponent, int):
            y = lambda x, _p=exponent: x * _p
            p = list(map(y, self.powers))
            f = pow(self.factor, exponent)
            names = FractionalDict((k, self.names[k] * Fraction(exponent, 1)) for k in self.names)
            return PhysicalUnit(names, f, p)
        elif isinstance(exponent, float):
            inv_exp = 1. / exponent
            rounded = int(np.floor(inv_exp + 0.5))
            if abs(inv_exp - rounded) < 1.e-10:
                if all(x % rounded == 0 for x in self.powers):
                    f = pow(self.factor, exponent)
                    p = [int(x / rounded) for x in self.powers]
                    if all(x % rounded == 0 for x in self.names.values()):
                        names = FractionalDict((k, v / rounded) for k, v in self.names.items())
                    else:
                        names = FractionalDict({str(f): 1} if f != 1. else {})
                        names.update({base_names[i]: p_i for i, p_i in enumerate(p)})
                    return PhysicalUnit(names, f, p)
                else:
                    raise UnitError('Illegal exponent %f' % exponent)
        raise UnitError('Only integer and inverse integer exponents allowed')

    def __hash__(self):
        """Return a hash based on factor, offset, and powers tuple."""
        # Powers list needs to be converted to a tuple to be hashable
        return hash((self.factor, self.offset, tuple(self.powers)))

    def conversion_factor_to(self, other):
        """Return conversion factor to another unit

        Parameters
        ----------
        other: PhysicalUnit
            Unit to compute conversion factor for

        Returns
        -------
        float
            Conversion factor

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.km.unit.conversion_factor_to(q.m.unit)
        1000.0
        """
        if self.powers != other.powers:
            raise UnitError(f'Incompatible units: cannot convert from {self} to {other}')
        if self.offset != other.offset and self.factor != other.factor:
            # This error might be too strict if only offset differs, conversion_tuple_to handles that.
            # Perhaps remove this check or refine it. For now, keep it but use f-string.
            raise UnitError(f'Unit conversion ({self.name} to {other.name}) with different offsets '
                            f'cannot be expressed as a simple multiplicative factor. Use conversion_tuple_to.')
        return self.factor / other.factor

    def conversion_tuple_to(self, other):
        """Return conversion factor and offset to another unit.

        The conversion is defined such that ``value_in_other = value_in_self * factor + offset``.

        Parameters
        ----------
        other: PhysicalUnit
            Unit to compute conversion factor and offset for

        Returns
        -------
        tuple[float, float]
            Tuple ``(factor, offset)``.

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.km.unit.conversion_tuple_to(q.m.unit)
        (1000.0, 0.0)
        >>> q.degC = add_composite_unit('degC', 1.0, 'K', offset=273.15) # Define Celsius relative to Kelvin
        >>> q.K.unit.conversion_tuple_to(q.degC.unit) # K to degC
        (1.0, -273.15)
        >>> q.degC.unit.conversion_tuple_to(q.K.unit) # degC to K
        (1.0, 273.15)
        """
        if self.powers != other.powers:
            raise UnitError(f'Incompatible unit for conversion from {self} to {other}')

        # Based on the definition: base = value * factor + offset
        # Let (f1, o1) be the conversion from 'self' (x) to base: base = x * f1 + o1
        # Let (f2, o2) be the conversion from 'other' (y) to base: base = y * f2 + o2
        # We want (F, O) such that y = x * F + O.
        # x * f1 + o1 = (x * F + O) * f2 + o2
        # x * f1 + o1 = x * F * f2 + O * f2 + o2
        # Equating coefficients:
        # f1 = F * f2  => F = f1 / f2
        # o1 = O * f2 + o2 => O = (o1 - o2) / f2
        # Note: Division by zero is possible if other.factor is 0, but this shouldn't
        # happen for physically meaningful units.

        f1, o1 = self.factor, self.offset
        f2, o2 = other.factor, other.offset

        factor = f1 / f2
        offset = (o1 - o2) / f2
        return factor, offset

    @property
    def to_dict(self) -> dict:
        """Export unit as dictionary.

        Returns
        -------
        dict
            Dictionary containing unit description ('name', 'verbosename', 'offset', 'factor', 'base_exponents').

        Notes
        -----
        The 'base_exponents' key contains a dictionary mapping base unit names to their integer exponents.
        """
        unit_dict = {'name': self.name,
                     'verbosename': self.verbosename,
                     'offset': self.offset,
                     'factor': self.factor
                     }
        b = self.baseunit
        p = b.powers
        base_dict = {}
        for i, exponent in enumerate(p):
            base_dict[base_names[i]] = exponent
        unit_dict['base_exponents'] = base_dict
        return unit_dict

    @property
    def to_json(self) -> str:
        """Export unit as JSON string.

        Returns
        -------
        str
            JSON string containing the unit description wrapped in a 'PhysicalUnit' key.

        Notes
        -----
        Uses `to_dict` internally for serialization.
        """
        json_unit = json.dumps({'PhysicalUnit': self.to_dict})
        return json_unit

    @staticmethod
    def from_dict(unit_dict) -> PhysicalUnit:
        """Retrieve PhysicalUnit from dict description.

        Parameters
        ----------
        unit_dict: dict
            PhysicalUnit stored as dict (matching the format from `to_dict`).

        Returns
        -------
        PhysicalUnit
            Retrieved PhysicalUnit instance.

        Raises
        ------
        UnitError
            If the unit name in the dictionary does not correspond to a known unit
            or if the dictionary data mismatches the found unit's definition.

        Notes
        -----
        This currently requires the unit to have been previously defined (e.g., via `addunit` or `add_composite_unit`).
        It does not create a new unit definition from the dictionary alone.
        """
        u = findunit(unit_dict['name'])
        # Check for consistency, but allow for float precision issues in factor/offset?
        # For now, requires exact match.
        if u.to_dict != unit_dict:
            # Provide more detailed error message if possible
            raise UnitError(f"Unit '{unit_dict['name']}' found, but its definition does not match the provided dict.")
        return u

    @staticmethod
    def from_json(json_unit) -> PhysicalUnit:
        """Retrieve PhysicalUnit from JSON string description.

        Parameters
        ----------
        json_unit: str
            PhysicalUnit encoded as JSON string (matching the format from `to_json`).

        Returns
        -------
        PhysicalUnit
            Retrieved PhysicalUnit instance.

        Raises
        ------
        UnitError
            If the JSON is invalid or the contained dictionary data is invalid per `from_dict`.
        """
        unit_dict = json.loads(json_unit)
        return PhysicalUnit.from_dict(unit_dict['PhysicalUnit'])


def addunit(unit: PhysicalUnit):
    """ Add a new PhysicalUnit entry to the global `unit_table`.

    Parameters
    -----------
    unit: PhysicalUnit
        PhysicalUnit object to add.

    Raises
    ------
    KeyError
        If a unit with the same name already exists in `unit_table`.
    """
    if unit.name in unit_table:
        raise KeyError(f'Unit {unit.name} already defined')
    unit_table[unit.name] = unit


unit_table: Dict[str, PhysicalUnit] = {}
# These are predefined base units 
base_names = ['m', 'kg', 's', 'A', 'K', 'mol', 'cd', 'rad', 'sr', 'Bit', 'currency']

addunit(PhysicalUnit('m', 1., [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Metre', verbosename='Metre',
        unece_code='MTR'))
addunit(PhysicalUnit('kg', 1, [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Kilogram', verbosename='Kilogram',
        unece_code='KGM'))
addunit(PhysicalUnit('s', 1., [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Second', verbosename='Second',
        unece_code='SEC'))
addunit(PhysicalUnit('A', 1., [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Ampere', verbosename='Ampere',
        unece_code='AMP'))
addunit(PhysicalUnit('K', 1., [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Kelvin', verbosename='Kelvin',
        unece_code='KEL'))
addunit(PhysicalUnit('mol', 1., [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Mole_(unit)', verbosename='Mol',
        unece_code='C34'))
addunit(PhysicalUnit('cd', 1., [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Candela', verbosename='Candela',
        unece_code='CDL'))
addunit(PhysicalUnit('rad', 1., [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Radian', verbosename='Radian',
        unece_code='C81'))
addunit(PhysicalUnit('sr', 1., [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        url='https://en.wikipedia.org/wiki/Steradian', verbosename='Steradian',
        unece_code='D27'))
addunit(PhysicalUnit('Bit', 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        url='https://en.wikipedia.org/wiki/Bit', verbosename='Bit',
        unece_code=''))
addunit(PhysicalUnit('currency', 1., [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        url='https://en.wikipedia.org/wiki/Currency', verbosename='Currency',
        unece_code=''))


def add_composite_unit(name, factor, units, offset=0, verbosename='', prefixed=False, url=''):
    """ Add new unit to the `unit_table`, defined relative to existing units.

    Parameters
    -----------
    name: str
        Name of the new unit (e.g., 'km', 'degC').
    factor: float
        Scaling factor relative to the base units derived from `units`.
    units: str
        String defining the base unit composition (e.g., 'm', 'K', 'm/s').
        This string is evaluated using the existing `unit_table`.
    offset: float, optional
        Additive offset factor (primarily for temperature scales). Default is 0.
    verbosename: str, optional
        A more descriptive name for the unit (e.g., 'Kilometre', 'degree Celsius'). Default is ''.
    prefixed: bool, optional
        Indicates if this unit is a standard prefixed version (like 'k'ilo, 'm'illi)
        of the unit defined by `units`. Affects the `baseunit` attribute. Default is False.
    url: str, optional
        A URL linking to more information about the unit. Default is ''.

    Returns
    -------
    str
        The name of the newly added unit.

    Raises
    ------
    KeyError
        If a unit with `name` already exists or if the `units` string is invalid or cannot be evaluated.
    ValueError
        If `factor` or `offset` is not numeric.
    """
    # Import locally to avoid circular dependency at module level
    from .quantity import PhysicalQuantity

    if name in unit_table:
        raise KeyError(f'Unit {name} already defined')
    # Parse composed units string
    try:
        potential_base = eval(units, unit_table)
        # Ensure we are working with a PhysicalUnit, not a PhysicalQuantity
        if isinstance(potential_base, PhysicalQuantity):
            baseunit = potential_base.unit
        elif isphysicalunit(potential_base):
            baseunit = potential_base
        else:
            # Handle cases where eval returns something unexpected (e.g., a number)
            raise TypeError(f"Evaluating '{units}' did not result in a PhysicalUnit or PhysicalQuantity.")
    except (SyntaxError, ValueError, NameError, TypeError) as e:
        # Catch eval errors and type errors from the check above
        raise KeyError(f'Invalid or unresolvable units string: {units} -> {e}')

    # Validate factor and offset values
    for value in (factor, offset):
        if not isinstance(value, (int, float)):
            raise ValueError('Factor and offset values have to be numeric')

    # Remove unwanted keys from unit_table
    for key in ['__builtins__', '__args__']:
        unit_table.pop(key, None)

    newunit = copy.deepcopy(baseunit)
    newunit.set_name(name)
    newunit.verbosename = verbosename
    newunit.baseunit = baseunit if prefixed else newunit
    newunit.prefixed = prefixed
    newunit.url = url
    newunit.factor *= factor
    newunit.offset += offset
    unit_table[name] = newunit

    return name


# Helper functions
# Restore cache decorator
@lru_cache(maxsize=None)
def findunit(unitname):
    """ Find and return a PhysicalUnit instance from its name string or object.

    Uses caching for performance. Handles simple fraction notation like '1/s'.

    Parameters
    ----------
    unitname: str or PhysicalUnit
        The name of the unit (e.g., 'm', 'km/h', 'N*m') or a PhysicalUnit object.

    Returns
    -------
    PhysicalUnit
        The corresponding PhysicalUnit instance.

    Raises
    ------
    UnitError
        If the input `unitname` is an empty string, cannot be parsed, or does not
        correspond to a known unit in the `unit_table`.

    Examples
    --------
    >>> findunit('mm')
    <PhysicalUnit mm>
    >>> findunit('1/s')
    <PhysicalUnit 1/s>
    """
    # Import locally to avoid circular dependency at module level
    from .quantity import PhysicalQuantity

    # Handle PhysicalUnit input directly (it's hashable and what we want)
    if isphysicalunit(unitname):
        return unitname

    if isinstance(unitname, str):
        if unitname == '':
            raise UnitError('Empty unit name is not valid')
        name = unitname.strip().replace('^', '**')
        # Handle simple fractions like 1/s, but avoid double-inverting things like 1/(m*s)
        # A more robust parser would be better than eval.
        if name.startswith('1/') and '(' not in name:
            name = f'({name[2:]})**-1'

        try:
            evaluated_unit = eval(name, unit_table)
        except NameError:
            raise UnitError(f'Invalid or unknown unit: {name}')
        except Exception as e:
            # Catch other potential eval errors
            raise UnitError(f'Error parsing unit string "{name}": {e}')

        # Check what eval returned - it might be a PhysicalQuantity
        if isphysicalunit(evaluated_unit):
            unit = evaluated_unit
        elif isinstance(evaluated_unit, PhysicalQuantity):
            unit = evaluated_unit.unit # Extract the unit part
        else:
            raise UnitError(f'Parsed unit string "{name}" did not result in a valid PhysicalUnit or PhysicalQuantity.')

        # Clean up namespace pollution from eval if necessary
        for cruft in ['__builtins__', '__args__']:
            try:
                del unit_table[cruft]
            except KeyError:
                pass
    elif isphysicalunit(unitname):
        # This case should be caught by the initial check, but kept for safety
        unit = unitname
    else:
        # Raise error for other unexpected types
        raise TypeError(f"findunit() argument must be a str or PhysicalUnit, not {type(unitname).__name__}")

    # Final check (redundant if logic above is correct, but safe)
    if not isphysicalunit(unit):
         raise UnitError(f'Could not resolve "{unitname}" to a PhysicalUnit.')
    return unit


def convertvalue(value, src_unit, target_unit):
    """ Convert a numerical value between compatible units.

    Handles both multiplicative factors and additive offsets (e.g., temperature scales).

    Parameters
    ----------
    value: number or array-like
        The numerical value(s) to convert.
    src_unit: PhysicalUnit
        The unit of the input `value`.
    target_unit: PhysicalUnit
        The unit to convert the `value` to.

    Returns
    -------
    number or array-like
        The converted value(s) in `target_unit`.

    Raises
    ------
    UnitError
        If `src_unit` and `target_unit` are incompatible (represent different physical dimensions)
        or if the conversion cannot be performed (e.g., involving incompatible offsets).

    Examples
    --------
    >>> from PhysicalQuantities import q
    >>> convertvalue(1, q.mm.unit, q.km.unit)
    1e-06
    >>> convertvalue(0, q.degC.unit, q.K.unit) # 0 degC to K
    273.15
    >>> convertvalue(273.15, q.K.unit, q.degC.unit) # 273.15 K to degC
    0.0
    """
    (factor, offset) = src_unit.conversion_tuple_to(target_unit)
    if isinstance(value, list):
        # Converting lists directly might be ambiguous (element-wise?); suggest using NumPy arrays.
        raise UnitError('Cannot convert units for a standard Python list; use NumPy arrays for element-wise conversion.')
    # Apply conversion: value_in_other = value_in_self * factor + offset
    # This works correctly for numbers and NumPy arrays due to broadcasting.
    return value * factor + offset


def isphysicalunit(x):
    """ Check if an object is an instance of the PhysicalUnit class.

    Parameters
    ----------
    x: Any
        Object to check.

    Returns
    -------
    bool
        True if `x` is a PhysicalUnit instance, False otherwise.
    """
    return isinstance(x, PhysicalUnit)
