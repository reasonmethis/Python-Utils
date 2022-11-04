from utilsmulti import run_with_processes_nokill
_calc_okchars = set('0123456789.+-*/() ')
_timeout = 0.5

def safe_eval_math_expr(expr: str):
    '''Returns the result of an expression, which must contain only math characters. 
    
    Returns None on error'''
    try:
        for ch in expr:
            if ch not in _calc_okchars:
                return
        res = eval(expr)
        #res = run_with_processes_nokill(_timeout, eval, expr)
        if type(res) not in (int, float, bool):
            raise TypeError #('Exprs can only be numerical or boolean')
        return res
    except Exception:
        return    
