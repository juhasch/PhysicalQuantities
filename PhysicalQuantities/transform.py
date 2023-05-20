"""Transform a single line by replacing inline physical units with 'pq.<unit>'"""
import tokenize
from tokenize import NAME, NUMBER, OP, TokenError
from PhysicalQuantities import q
import io


def add_pq_prefix(token: str, prefix: str = ' pq.') -> str:
    """Add prefix 'pq.' if valid unit was found

    Parameters
    ----------
    token
        Token representing potential unit name
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
    """Transform a single line by replacing inline physical units with 'pq.<unit>',
       i.e. '1m' -> '1* pq.m'
    """
    string_io = io.StringIO(line)
    g = tokenize.generate_tokens(string_io.readline)
    tokenlist = []
    result = []
    token_type = []

    try:
        for t in g:
            tokenlist.append(t)
            token_type.append(t[0])
    except TokenError:
        pass

    i = 0
    while i < len(tokenlist):
        lo = slice(i, i + 4)
        sh = slice(i, i + 2)
        if token_type[lo] == [NUMBER, NAME, OP, NAME]:
            result.append((tokenlist[i][0], '('+tokenlist[i+0][1]))
            newtokval = add_pq_prefix(tokenlist[i+1][1], '*pq.')
            result.append((tokenlist[i+1][0], newtokval + ')'))
            result.append((tokenlist[i+2][0], tokenlist[i+2][1]))
            newtokval = add_pq_prefix(tokenlist[i+3][1])
            result.append((tokenlist[i+3][0], newtokval))
            i += 4
        elif token_type[sh] == [NUMBER, NAME]:
            if tokenlist[i+2].string in ['**']:
                # apply exponent only unit not number
                result.append((tokenlist[i][0], 'PhysicalQuantity(' + tokenlist[i + 0][1]))
                newtokval = add_pq_prefix(tokenlist[i + 1][1], ',"')
                result.append((tokenlist[i + 1][0], newtokval + tokenlist[i+2].string + tokenlist[i+3].string + '")'))
                i += 4
            else:
                result.append((tokenlist[i][0], '('+tokenlist[i+0][1]))
                newtokval = add_pq_prefix(tokenlist[i+1][1], '*pq.')
                result.append((tokenlist[i+1][0], newtokval + ')'))
                i += 2
        else:
            result.append(tokenlist[i])
            i += 1
    line = tokenize.untokenize(result)
    return line
