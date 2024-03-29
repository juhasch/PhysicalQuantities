# Extend prefix range of prefixed units from engineering (1e+-12) to full (1e+-24)
import PhysicalQuantities
from .prefixes import addprefixed

addprefixed('m', prefixrange='full')
addprefixed('g', prefixrange='full')
addprefixed('s', prefixrange='full')
addprefixed('A', prefixrange='full')
addprefixed('K', prefixrange='full')
addprefixed('mol', prefixrange='full')
addprefixed('cd', prefixrange='full')
addprefixed('rad', prefixrange='full')
addprefixed('sr', prefixrange='full')
addprefixed('Hz', prefixrange='full')
addprefixed('N', prefixrange='full')
addprefixed('Pa', prefixrange='full')
addprefixed('J', prefixrange='full')
addprefixed('W', prefixrange='full')
addprefixed('C', prefixrange='full')
addprefixed('V', prefixrange='full')
addprefixed('F', prefixrange='full')
addprefixed('Ohm', prefixrange='full')
addprefixed('S', prefixrange='full')
addprefixed('Wb', prefixrange='full')
addprefixed('T', prefixrange='full')
addprefixed('H', prefixrange='full')
addprefixed('lm', prefixrange='full')
addprefixed('lx', prefixrange='full')

PhysicalQuantities.q.update()
