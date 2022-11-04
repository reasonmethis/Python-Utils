from typing import Iterable
from coinator import cn
import utilsstrings as ust

def extract_num_token_combos(st: str):
    part_l = st.split()
    typ_s = ''
    for part in part_l:
        try:
            tmp = float(part)
            typ_s += 'n'
        except:
            if cn.is_sym(part):
                typ_s += 't'
            else:
                typ_s += 'o'
    return list(ust.find_all(typ_s, 'nt')), part_l

def extract_tokens_after_nums(st: str) -> list[str]:
    ind_l, part_l = extract_num_token_combos(st)
    sym_l = []
    for ind in ind_l:
        sym = part_l[ind + 1].upper()  
        if sym not in sym_l:
            sym_l.append(sym)
    return sym_l

def extract_tokens_betw_spaces(st: str) -> set[str]:
    '''Extract symbol names'''
    syms = set()
    for wrd in st.split(): 
        wrd = wrd.upper()
        if cn.is_sym(wrd):
            syms.add(wrd)
    return syms

def extract_tokens_betw_spaces_from_strs(st_l: Iterable) -> set[str]:
    '''Extract symbol names from a bunch of strings, returns a set'''
    syms = set()
    for st in st_l:
        syms.update(extract_tokens_betw_spaces(st))
    return syms

from typing import Iterable

def extract_tokens_from_exprs(named_expr_l: Iterable[str]) -> set[str]:
    '''extract token names to query prices for '''
    names = set()
    all_expr_l = [] #collect all expressions to extract tokens from 
    for expr in named_expr_l:
        if expr[0] in ['*', '$']:
            expr = expr[1:] #to be able to extract token name from for example '*ALEPH'
        item_spl = expr.split(' = ')
        if len(item_spl) > 1: #then must be 2
            names.add(item_spl[0]) #this is not a token to look up then but an expression name
            expr = item_spl[1]
        all_expr_l.append(expr)

    return {sym for sym in extract_tokens_betw_spaces_from_strs(all_expr_l) if sym not in names}

if __name__ == '__main__':
    st = '''2022-05-26 11:01:40 UTC: Traded 293 USDT for 3358 UST 
2022-05-26 17:50:00 UTC: From 298.51068599999996 SPEC To 2000.286947 UST
2022-06-07 05:41:06 UTC: Used 1000 USDC to short 500 GMT on Mango and supply 500 GMT on Francium (GMT = $0.9521)
2022-06-07 08:13:36 UTC: Undid previous (funding rate was -80+%), and longed 524 GMT on Mango, shorted on Solend, cur equity 559 + 423 = 982 (GMT = $0.9550)
2022-06-16 18:44:02 UTC: Swap 2906 TOMB for 711.76 FTM (FTM = $0.2318, TOMB = $0.0566)
2022-06-16 18:53:34 UTC: Staked 711.76 WFTM to Genesis, 0.5% fee, APR 56% (FTM = $0.2308)
'''
    ind_l, part_l = extract_num_token_combos(st)
    for ind in ind_l:
        print(part_l[ind], part_l[ind + 1])
    print(extract_tokens_after_nums('swap 2 ust for 3 lUNA UST'))