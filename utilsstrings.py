from re import split
from typing import Callable, Iterable
import json
from math import log10, floor

def vars_to_json(**kwargs): 
    return json.dumps(kwargs)

def st_contains(st: str, substs: Iterable[str]) -> bool:
    for subst in substs:
        if subst not in st:
            return False
    return True

def to_float_or_none(st:str):
    try:
        return float(st)
    except:
        return None

def splitstrip(st: str, sep: str=None) -> list[str]:
    '''Split the string and remove spaces from each part'''
    return [x.strip() for x in st.split(sep)]

def part_type_st(st: str, gettype: Callable, getparts: Callable=splitstrip) -> str:
    type_s = ''
    for part in getparts(st):
        type_s += gettype(part)
    return type_s

def split_string(string, delimiters, incl_delimiters=False):
    """Splits a string by a list of delimiters. Delimiters are found on a first come first serve 
    basis in the list - for example '1>=2' will be split into '1', '2' if delimiters=['>=','>']
    Args:
        string (str): string to be split
        delimiters (list): list of delimiters
    Returns:
        list: list of split strings
    """
    #https://datagy.io/python-split-string-multiple-delimiters/
    pattern = '|'.join(delimiters)
    if incl_delimiters:
        pattern = '(' + pattern + ')'
    return split(pattern, string)

def pretty_concat_strings(st_l, sep_s='  ', just=20, width=110):
    '''Combine strings into one string for printing, making sure to space them nicely
    and not to break up a string across lines'''
    lenprevrows = 0
    res_s = ''
    for st in st_l:
        add_s = st + sep_s
        if just is not None:
            add_s = add_s.ljust(just)
        if len(res_s) - lenprevrows + len(add_s) >= width:
            res_s +='\n'
            lenprevrows = len(res_s)
        res_s += add_s
    return res_s

def find_all(st: str, sub: str):
    '''Yield all indices where the substring is found in the string'''
    start = 0
    while True:
        start = st.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def part_till_substr(st: str, subst: str, start=0):
    ind_till = st.find(subst, start)
    if ind_till == -1:
        raise ValueError('Terminator substring not found.')
        return st[start:]
    return st[start:ind_till]

def part_btw_substrs(st: str, subst1: str, subst2: str, start=0):
    ind_from = st.find(subst1, start) + 1
    if ind_from == 0:
        raise ValueError('First substring not found.')
    ind_till = st.find(subst2, ind_from)
    if ind_till == -1:
        raise ValueError('Terminator substring not found.')
    return st[ind_from:ind_till]

def part_before_part(st: str, part_next: str, getparts: Callable=splitstrip) -> str:
    '''Converts st to an iterable (using getparts - splitstrip by default), iterates through it
    and returns the element right before the element specified by part_next, or None.'''
    part_prev = None
    for part in getparts(st):
        if part == part_next:
            return part_prev
        part_prev = part
    return None

def replace_subst(st: str, subst:str, newsubst: str, start=0) -> str:
    '''Replace next occurrence of substring'''
    ind = st.find(subst, start)
    if ind == -1:
        return st
    return st[:ind] + newsubst + st[ind + len(subst):]

def float2st(x: float, n_afterperiod: int, n_minsigfigs=0, strip_zeros=False):
    nzeroes_afterperiod = -floor(log10(abs(x))) - 1
    
    return str(round(x, max(n_afterperiod, nzeroes_afterperiod + n_minsigfigs)))

if __name__ == '__main__':
    print(float2st(-0.0006666, 2, 1))
    i=1
    #a=2;b='4567'
    #print(json.dumps(dict(a=a, b=b)))
    #print(split_string('fg >= %" == 567', ['>', '>=', '<=','>', '<']))
