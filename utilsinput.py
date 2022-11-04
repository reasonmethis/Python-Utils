
#This stackexchange answer (jan 2022) claims to provide cross-platform blocking
#and non-blocking keyboard input functions, seems to be written quite professionally:
#https://stackoverflow.com/a/70664652

import msvcrt #for Windows, see comment at the top
from typing import Collection, Container, Iterable 
from collections import namedtuple

_escape_chars = frozenset(('\x00', '\xe0'))
_specialkeys_class = namedtuple('_specialkeys_class', ['esc', 'delete'])
key = _specialkeys_class('\x1b', '\x00\x53') #so can use key.esc, key.del, etc.

def getkeystroke():
    key = msvcrt.getwch()
    if key in _escape_chars:
        key += msvcrt.getwch()
    #print(key_to_hex(key))
    return key

def flushbuf():
    while msvcrt.kbhit():
        msvcrt.getch()

def key_to_hex(key):
    return '\\x' + '\\x'.join(map('{:02x}'.format, map(ord, key)))

def keypressed(keys: Collection[str] = None, flush: bool = False) -> str:
    '''Return the pressed key if one of the specified keys has been pressed. If multiple 
    keys have been pressed, read them and remove from queue until a matching key is found 

    Args:
        keys: The keys to check for. If None, any key will do.
        flush: If True, flush the input buffer at the end 
    
    Return:
        The key that was pressed or None.

    Notes: 
        adapted from https://stackoverflow.com/a/70664652
    '''
    while msvcrt.kbhit():
        keystroke = getkeystroke()
        if keys is None or keystroke in keys:
            if flush:
                flushbuf()
            return keystroke
    return None

def whichkey():
    if not msvcrt.kbhit():
        return None
    return getkeystroke()
    
def printkey():
    flushbuf()
    print(key_to_hex(getkeystroke()))

def wait_for_option(key_d):
    while True:
        #k = keyboard.read_key(True) #True prevents keypress from propagating - doesn't work 
        k = msvcrt.getch() #should I be using getwch, as the above answer does? or 
        k = k.decode('utf-8')
        if k in key_d:
            return key_d[k]

def promptuser(prompt_s, failmsg_s, process_func, justvalidate=True):
    while True:
        st = input(prompt_s)
        try:
            processedinput = process_func(st)
            return st if justvalidate else processedinput
        except:
            print(failmsg_s)

class menu:
    _option_class = namedtuple('_option_class', ['txt', 'actcode', 'key', 'keyname'])
    def __init__(self, firstnumkey=1) -> None:
        self.opt_l = [] 
        self.opt_d = {} #{key pressed: actioncode}
        self.numkeylast = firstnumkey - 1

    def addoption(self, txt, actioncode, key=None, keyname_s=None):
        if key is None:
            self.numkeylast += 1
            key = str(self.numkeylast)
        if keyname_s is None:
            keyname_s = key

        self.opt_d[key] = actioncode
        self.opt_l.append(menu._option_class(txt, actioncode, key, keyname_s))
    
    def addexitoption(self, actioncode, txt='Exit menu'):
        self.addoption(txt, actioncode, key=key.esc, keyname_s='ESC')

    @property
    def menu_s(self):
        res = ''
        for opt in self.opt_l:
            res += f'{opt.keyname} - {opt.txt}\n'
        return res
    
    def askuser(self, end='\n'):
        print(self.menu_s, end='') #by default print one empty line after the menu
        choice = wait_for_option(self.opt_d)
        print(end, end='')
        return choice
        
if __name__ == '__main__':
    print('Press a key and it will be printed out.')
    while True:
        if k := whichkey():
            print('Pressed key ' + key_to_hex(k) + ': ' + k)

