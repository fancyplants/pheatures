import sys

def getch():
    import termios
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\u0003':
                sys.exit(0)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()

import curses
import os

def main(win):
    win.nodelay(True)
    key=""
    win.clear()                
    win.addstr("Detected key:")
    while 1:          
        try:                 
           key = win.getkey()         
           win.clear()                
           win.addstr("Detected key:")
           win.addstr(str(key)) 
           if key == os.linesep:
              break           
        except Exception as e:
           # No input   
           pass         

curses.wrapper(main)

