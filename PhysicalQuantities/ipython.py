# -*- coding: utf-8 -*-
""" IPython extension for physical quantity input """

# Original author: Georg Brandl <georg@python.org>.
#                  https://bitbucket.org/birkenfeld/ipython-physics

import re
import sys

from IPython.core.inputtransformer import StatelessInputTransformer
from IPython.core.inputtransformer import CoroutineInputTransformer
from IPython.display import display, Math, Latex, HTML

import PhysicalQuantities as pq

name = r'([_a-zA-Z]\w*)'
number = r'(-?[\d0-9.eE-]+)'
unit = r'([a-zA-Z1°µ][a-zA-Z0-9°µ/*^-]*)'
quantity = number + r'(?:\s+\+\/-\s+' + number + ')?' + r'\s+' + unit

inline_unit_re = re.compile(r'\((%s)\)' % quantity)

nice_assign_re = re.compile(r'^%s\s*=\s*(%s)$' % (name, quantity))
quantity_re = re.compile(quantity)
subst_re = re.compile(r'\?' + name)

# sort units after length for Regex matching
_li = sorted(pq.unit_table,key=len)
_unit_list = ''
for unit in _li[::-1]:
    _unit_list += unit + '|'
_unit_list = _unit_list[0:-1]# + ']'

# regex for finding units and quoted strings
stringmatch = r'(["\'])(?:(?=(\\?))\2.)*?\1'
number = r'(?<![\w])(-?[0-9]*\.?[0-9]*[eE]?-?[0-9]*)'
number1 = r'(?<![\w])(-?[0-9]+\.?[0-9]*[eE]?-?[0-9]*)'
number2 = r'(?<![\w])(-?[0-9]*\.?[0-9]+[eE]?-?[0-9]*)'
match0 = stringmatch + '|' + number1 + r'(\s*)' + '(' + _unit_list + ')' #+ r'(?:\W+|$)'
match1 = stringmatch + '|' + number2 + r'(\s*)' + '(' + _unit_list + ')' #+ r'(?:\W+|$)'
match2 = stringmatch + '|' + number + r'(\s*)' + '([' + _unit_list + ']\*\*[2-9]+' + ')' #+  r'(?:\W+|$)'
match3 = stringmatch + '|' + number + r'(\s*)' + '([' + _unit_list + ']\/['  + _unit_list + '])'# +  r'(?:\W+|$)'

line_match0 = re.compile(match0)
line_match1 = re.compile(match1)
line_match2 = re.compile(match2)
line_match3 = re.compile(match3)

def replace_inline(m):
    """Replace an inline unit expression by valid Python code
    """
    if (m):
#        print m.groups()
        if m.group(3) == None or m.group(3) == '':
            return m.group(0)
    return 'PhysicalQuantity('+ m.group(3)+',\'' + m.group(5) + '\')'

@StatelessInputTransformer.wrap
def _transform(line):
    line = line_match3.sub(replace_inline, line) # unit**n
#    print "3:%s" % line
    line = line_match2.sub(replace_inline, line) # unit/unit
#    print "2:%s" % line
    line = line_match1.sub(replace_inline, line)
#    print "1:%s" % line
    line = line_match0.sub(replace_inline, line)
#    print "0:%s" % line    
    return line

__transformer = _transform()


def load_ipython_extension(ip):
    global __transformer
    ip.input_transformer_manager.logical_line_transforms.insert(0, __transformer)

    ip.user_ns['PhysicalQuantity'] = pq.PhysicalQuantity

def unload_ipython_extension(ip):
    global __transformer
    if type(__transformer) is StatelessInputTransformer:
        ip.input_transformer_manager.logical_line_transforms.remove(__transformer)
        ip.user_ns.pop('PhysicalQuantity')
