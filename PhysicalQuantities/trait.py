""" PhysicalTrait class definition

TODO: What is a PhysicalTrait, and why is it useful ?

Example
-------

from .trait.quantization import E96
resistor = PhysicalTrait(4.7, unit='kOhm', domain='positive', description='My resistor`, quantization=E96)

resistor.value = 1234  # raises TraitError
resistor.value = 10  # OK


"""

from traitlets import TraitError, TraitType

from .unit import PhysicalUnit

__all__ = ['PhysicalTrait']


class PhysicalTrait(TraitType):
    """ Physical Trait - Object with physical traits like unit, etc.

    """

    def __init__(self, value, unit, domain, desription, **kwargs):
        """
        Parameters
        ----------
        value
            Value of trait
        domain
            Domain (negative, positive)
        unit: PhysicalUnit
            Unit of the trait
        description: str
            Description of the trait
        quantization: float|array
            Quantization step if scalar or allowed values if array

        """
        super().__init__(**kwargs)
        self.value = value
        self.domain = domain
        self.unit = unit
        self.description = desription
        # TODO: traitlets default argument
        # TODO: check args

    def _validate(self):
        """Validate parameters"""
        if self.domain == 'negative':
            if any(self.value > 0):
                raise TraitError('Domain allows only negative values')
        elif self.domain == 'strictly-negative':
            if any(self.value > 0):
                raise TraitError('Domain allows only strictly negative values')
        elif self.domain == 'positive':
            if any(self.value < 0):
                raise TraitError('Domain allows only positive values')
        elif self.domain == 'negative':
            if any(self.value <= 0):
                raise TraitError('Domain allows only strictly positive values')
