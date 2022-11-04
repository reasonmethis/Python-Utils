import win32gui as wig
import win32api, win32con
import autoit as au
import pyautogui as pg
#import pyautogui as pag
MOUSEEVENTF_LEFTCLICK = win32con.MOUSEEVENTF_LEFTDOWN + win32con.MOUSEEVENTF_LEFTUP
#autoit.control_click("[Class:Chrome_WidgetWin_1]", 
#"Intermediate D3D Window1", x=1176, y=576)
#autoit.control_click('[Class:Notepad]', 'Edit1', x=13, y=47)
#autoit.control_click_by_handle(0x00030C82, 0x000E0C56, x=33, y=17)

def locate_center(img_fname, grayscale=True, confidence=0.9):
    try:
        return pg.locateCenterOnScreen(img_fname, grayscale=grayscale, confidence=confidence)
    except:
        return None

def click(x, y, delay=0.1):
    #can also use pag.click
    win32api.SetCursorPos((x, y))#MOUSEEVENTF_LEFTCLICK
    win32api.mouse_event(MOUSEEVENTF_LEFTCLICK, 0, 0)
    #time.sleep(delay) #This pauses the script for 0.1 seconds
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def activatewin(hw):
    au.win_activate_by_handle(hw)
    au.win_wait_active_by_handle(hw, 3)

def wintitle(hw):
    try:
        return wig.GetWindowText(hw)
    except:
        return None

#locateOnScreen(image, confidence=0.7)
#returns box coordinates as it found the image at a lower confidence

'''
autoit.run("notepad.exe")
autoit.win_wait_active("[CLASS:Notepad]", 3)
autoit.control_send("[CLASS:Notepad]", "Edit1", "hello world{!}")
autoit.win_close("[CLASS:Notepad]")
autoit.control_click("[Class:#32770]", "Button2")
'''

def get_visible_windows(): #wndtxt=None, substr=True):
    def do(hwnd, ctx):
        if wig.IsWindowVisible(hwnd):
            win_l.append(hwnd)
    win_l = []
    wig.EnumWindows(do, None)
    return win_l

def find_win_by_substr(substr, hwnd_l=None):
    '''Return win whose title contains the substring. Second param specifies the list of windows
    to search in. If it's not specified, search in visible windows. Returns None if not found'''
    if hwnd_l is None:
        hwnd_l = get_visible_windows()
    for hw in hwnd_l:
        txt = wig.GetWindowText(hw)
        if substr in txt:
            return hw

def find_wins_by_substrs(substr_l, hwnd_l=None):
    '''For each str in substring list, return win whose title contains str (or None if not found )
    Second param specifies the list of windows
    to search in. If it's not specified, search in visible windows. Returns list with same size 
    as the substring list'''
    if hwnd_l is None:
        hwnd_l = get_visible_windows()
    
    res_l = []
    titl_d = {}
    for substr in substr_l:
        for hw in hwnd_l:
            try:
                titl = titl_d[hw]
            except KeyError:
                titl = titl_d[hw] = wig.GetWindowText(hw)
            if substr in titl:
                res_l.append(hw)
                break
        else:
            res_l.append(None)
    return res_l
