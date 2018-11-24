""" IPython extension for physical quantity input"""

import io
import tokenize
from tokenize import NAME, NUMBER, OP

import PhysicalQuantities
from PhysicalQuantities import q
from IPython.core.inputtransformer import StatelessInputTransformer


# Flag for multiline comments
within_comment = False


def add_pq_prefix(token: str, prefix: str=' pq.') -> str:
    """Add prefix 'pq.' if valid unit was found

    Parameters
    ----------
    token
        Token representing potenital unit name
    prefix
        Prefix to add, default is ' pq.'

    Returns
    -------
        Token with 'pq.' prefix added
    """
    if token in q.table.keys():
        return prefix + token
    return token


def transform_line(line=''):
    global within_comment
    if line.count('"""') %2 or line.count("'''") %2:
        within_comment = not within_comment
        return

    if within_comment:
        return

    string_io = io.StringIO(line)
    g = tokenize.generate_tokens(string_io.readline)

    tokenlist = []
    result = []
    token_type = []

    for t in g:
        tokenlist.append(t)
        token_type.append(t[0])

    i = 0
    while i < len(tokenlist):
        lo = slice(i, i + 4)
        sh = slice(i, i + 2)
        if token_type[lo] == [NUMBER, NAME, OP, NAME]:
            result.append(tokenlist[i])
            newtokval = add_pq_prefix(tokenlist[i+1][1], '* pq.')
            result.append((tokenlist[i+1][0], newtokval))
            result.append((tokenlist[i+2][0], tokenlist[i+2][1]))
            newtokval = add_pq_prefix(tokenlist[i+3][1])
            result.append((tokenlist[i+3][0], newtokval))
            i += 4
        elif token_type[sh] == [NUMBER, NAME]:
            result.append(tokenlist[i])
            newtokval = add_pq_prefix(tokenlist[i+1][1], '* pq.')
            result.append((tokenlist[i+1][0], newtokval))
            i += 2
        else:
            result.append(tokenlist[i])
            i += 1
    line = tokenize.untokenize(result)
    return line


def transform(lines):
    result = []
    for line in lines:
        result.append(transform_line(line))
    return result


def load_ipython_extension(ip):  # pragma: no cover
    global within_comment
    within_comment = False
    ip.input_transformers_cleanup.append(transform)
    ip.user_ns['pq'] = PhysicalQuantities.q


def unload_ipython_extension(ip):  # pragma: no cover
    if type(__transformer) is StatelessInputTransformer:
        ip.input_transformers_cleanup.remove(transform)
        ip.user_ns.pop('pq')
