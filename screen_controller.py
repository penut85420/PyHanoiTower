import ctypes
import os
import sys

if os.name == 'nt':
    import msvcrt
    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]

class ScreenController:
    def __init__(self):
        if os.name == 'nt':
            self.handle = ctypes.windll.kernel32.GetStdHandle(ctypes.c_long(-11))
    
    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            sys.stdout.write(chr(27) + '[2J')

    def move(self, y, x):
        if os.name == 'nt':
            value = x + (y << 16)
            ctypes.windll.kernel32.SetConsoleCursorPosition(self.handle, ctypes.c_ulong(value))
        elif os.name == 'posix':
            sys.stdout.write("\033[%d;%dH" % (y, x))
            sys.stdout.flush()
    
    def hide_cursor(self):
        if os.name == 'nt':
            ci = _CursorInfo()
            ctypes.windll.kernel32.GetConsoleCursorInfo(self.handle, ctypes.byref(ci))
            ci.visible = False
            ctypes.windll.kernel32.SetConsoleCursorInfo(self.handle, ctypes.byref(ci))
        elif os.name == 'posix':
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

    def show_cursor(self):
        if os.name == 'nt':
            ci = _CursorInfo()
            ctypes.windll.kernel32.GetConsoleCursorInfo(self.handle, ctypes.byref(ci))
            ci.visible = True
            ctypes.windll.kernel32.SetConsoleCursorInfo(self.handle, ctypes.byref(ci))
        elif os.name == 'posix':
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()
