# -*- coding: utf-8 -*-
""" IPython extension for physical quantity input """

# Original author: Georg Brandl <georg@python.org>.
#                  https://bitbucket.org/birkenfeld/ipython-physics

import re
from IPython.core.inputtransformer import StatelessInputTransformer
from PhysicalQuantities import PhysicalQuantity, dBQuantity
from PhysicalQuantities.dBQuantity import dB_unit_table
from PhysicalQuantities import unit_table


name = r'([_a-zA-Z]\w*)'
number = r'-?([\d0-9.eE-]+)'
unit = r'([a-zA-Z1°µ][a-zA-Z0-9°µ/*^-]*)'
quantity = number + r'(?:\s+\+\/-\s+' + number + ')?' + r'\s+' + unit

inline_unit_re = re.compile(r'\((%s)\)' % quantity)

nice_assign_re = re.compile(r'^%s\s*=\s*(%s)$' % (name, quantity))
quantity_re = re.compile(quantity)
subst_re = re.compile(r'\?' + name)

# sort units after length for Regex matching
_li = sorted(unit_table, key=len)
_unit_list = ''
for unit in _li[::-1]:
    _unit_list += unit + '|'
_unit_list = _unit_list[0:-1]

# regex for finding units and quoted strings
stringmatch = r'(["\'])(?:(?=(\\?))\2.)*?\1'
number  = r'(?<![\w])([0-9]*\.?[0-9]*[eE]?-?[0-9]*)'
number1 = r'(?<![\w])([0-9]+\.?[0-9]*[eE]?-?[0-9]*)'
number2 = r'(?<![\w])([0-9]*\.?[0-9]+[eE]?-?[0-9]*)'
match0 = stringmatch + '|' + number1 + r'(\s*)' + '(' + _unit_list + ')'
match1 = stringmatch + '|' + number2 + r'(\s*)' + '(' + _unit_list + ')'
match2 = stringmatch + '|' + number + r'(\s*)' + '(' + _unit_list + ')(\*\*-?[1-9]+' + ')'
match3 = stringmatch + '|' + number + r'(\s*)' + '(' + _unit_list + ')\/(' + _unit_list + ')'

line_match0 = re.compile(match0)
line_match1 = re.compile(match1)
line_match2 = re.compile(match2)
line_match3 = re.compile(match3)

# =========================================
# dB
# sort units after length for Regex matching
# regex: number + space + dB-unit
# valid: 0dBm, 0 dBm, 0. dBm
# invalid: 0.dBm
number = r'(-?[\d0-9-.]+)'

_li = sorted(list(dB_unit_table.keys()),key=len, reverse=True)

_dB_unit_list = '('
for x in _li:
    _dB_unit_list += x + '|'
_dB_unit_list = _dB_unit_list.strip('|') + ')'

# regex for finding units and quoted strings
number = r'(?<!\w)-?([\d0-9.]+[\d0-9eE-|x]*)'
match = stringmatch+ '|' + number + r'(\s*)' + _dB_unit_list
dB_line_match = re.compile(match)

# regex to match unit after it has been found using line_match
number = r'(-?[\d0-9-]+' + r'-?[\d0-9.eE-]*)'
match = number + r'(.\s|\s*)' + _dB_unit_list
dB_unit_match = re.compile(match)


def dB_replace_inline(ml):
    """Replace an inline unit expression by valid Python code
    """
    if ml.group()[0][0] in '"\'':
        return ml.group()

    def replace_unit(mo):
        try:
            return "dBQuantity(" + mo.group(1) + ", '" + mo.group(3) + "', islog=True)"
        except KeyError:
            return mo.group()

    return dB_unit_match.sub(replace_unit, ml.group())

# =========================================


def replace_inline(m):
    """Replace an inline unit expression by valid Python code
    """
    if m:
        if m.group(3) is None or m.group(3) == '':
            return m.group(0)
    return 'PhysicalQuantity(' + m.group(3)+',\'' + m.group(5) + '\')'


def replace_inline1(m):
    """Replace an inline unit expression by valid Python code
    """
    if m:
        if m.group(3) is None or m.group(3) == '':
            return m.group(0)
    return 'PhysicalQuantity(' + m.group(3)+',\'' + m.group(5) + m.group(6) + '\')'


def replace_inline2(m):
    """Replace an inline unit expression by valid Python code
    """
    if m:
        if m.group(3) is None or m.group(3) == '':
            return m.group(0)
    return 'PhysicalQuantity(' + m.group(3)+',\'' + m.group(5) + '/' + m.group(6) + '\')'


@StatelessInputTransformer.wrap
def _transform(line):
    line = line_match3.sub(replace_inline2, line)  # unit/unit
    line = line_match2.sub(replace_inline1, line)  # unit**n
    line = line_match1.sub(replace_inline, line)
#    print(':', line)
    line = line_match0.sub(replace_inline, line)
    line = dB_line_match.sub(dB_replace_inline, line)
    return line

__transformer = _transform()


def load_ipython_extension(ip):
    global __transformer
    ip.input_transformer_manager.logical_line_transforms.insert(0, __transformer)

    ip.user_ns['PhysicalQuantity'] = PhysicalQuantity
    ip.user_ns['dBQuantity'] = dBQuantity


def unload_ipython_extension(ip):
    global __transformer
    if type(__transformer) is StatelessInputTransformer:
        ip.input_transformer_manager.logical_line_transforms.remove(__transformer)
        ip.user_ns.pop('PhysicalQuantity')
        ip.user_ns.pop('dBQuantity')
