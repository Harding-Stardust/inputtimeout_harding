#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is a modified version of inputimeout (https://pypi.org/project/inputtimeout)
With the following mods:
correct spelling inputimeout -> inputtimeout
docstrings
type hints
default values
each keypress adds time (20 seconds) to the timeout so we won't interupt the user when he/she is typing (Only on Windows)
"""

__version__ = 230702130848
__author__ = "Harding"
__description__ = __doc__
__copyright__ = "Copyright 2023"
__credits__ = ["inputimeout: https://pypi.org/project/inputimeout"]
__license__ = "GPL"
__maintainer__ = "Harding"
__email__ = "not.at.the.moment@example.com"
__status__ = "Development"

from typing import Union as _Union
from types import ModuleType as _ModuleType
import sys

_DEFAULT_TIMEOUT_IN_SECONDS: float = 30.0
_DEFAULT_RETURN_VALUE: str = 'Timeout occured'
_DEFAULT_ERROR_MESSAGE: str = " No user input, defaulted to "
_CHECK_INTERVAL: float = 0.05

_CR = '\r'
_LF = '\n'
_CTRL_Z = '\x1A'
_CTRL_C = '\003'
_CRLF = _CR + _LF
_BACKSPACE = '\b'

def _reload(arg_module: _Union[str, _ModuleType, None] = None):
    ''' Internal function. During development, this is nice to have '''

    import importlib

    l_module: str = arg_module if isinstance(arg_module, str) else getattr(arg_module, '__name__', __name__)
    return importlib.reload(sys.modules[l_module])

def _posix_inputtimeout(arg_prompt: str = '', arg_timeout_in_seconds: float = _DEFAULT_TIMEOUT_IN_SECONDS, arg_default_return_value: str = _DEFAULT_RETURN_VALUE) -> str:
    ''' POSIX implementation using select() '''
    print(arg_prompt, file=sys.stdout, flush=True, end='')
    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ)
    events = sel.select(arg_timeout_in_seconds)

    if events:
        key, _ = events[0]
        return key.fileobj.readline().rstrip(_LF)

    termios.tcflush(sys.stdin, termios.TCIFLUSH)
    print(_DEFAULT_ERROR_MESSAGE + f"'{arg_default_return_value}'", file=sys.stdout, flush=True)
    return arg_default_return_value

def _win_inputtimeout(arg_prompt: str = '', arg_timeout_in_seconds: float = _DEFAULT_TIMEOUT_IN_SECONDS, arg_default_return_value: str = _DEFAULT_RETURN_VALUE) -> str:
    ''' Windows implementation using getwche()

        If you press Ctrl + C then the Exception KeyboardInterrupt is raised

    '''
    print(arg_prompt, file=sys.stdout, flush=True, end='')
    begin: float = time.monotonic()
    end: float = begin + arg_timeout_in_seconds
    line: str = ''

    while time.monotonic() < end:
        if msvcrt.kbhit():
            c = msvcrt.getwche()
            end = time.monotonic() + 20 # Each key press adds to the timeout so we won't interupt the user if he/she is typing. OBS! This will make the POSIX and Windows version work differently!
            if c in (_CR, _LF, _CTRL_Z):
                print(_CRLF, file=sys.stdout, flush=True)
                return line
            if c == _CTRL_C:
                raise KeyboardInterrupt
            if c == _BACKSPACE:
                line = line[:-1]
                cover = ' ' * len(arg_prompt + line + ' ')
                print(''.join([_CR, cover, _CR, arg_prompt, line]), file=sys.stdout, flush=True, end='')
            else:
                line += c
                # return line # TODO: test with only 1 keypress as choice.com
        time.sleep(_CHECK_INTERVAL)

    print(f"{_DEFAULT_ERROR_MESSAGE} '{arg_default_return_value}'", file=sys.stdout, flush=True)
    return arg_default_return_value

if "__main__" == __name__:
    import os
    my_module_name: str = os.path.basename(__file__)[:-3]
    print("This module is not usable from the console, use it like this:")
    print()
    print(f"import {my_module_name}")
    print(f"username = {my_module_name}.inputtimeout(arg_prompt='You have 10 seconds to enter your name >> ', arg_timeout_in_seconds=10.0, arg_default_return_value='You seems to have forgotten your name')")
    print("print(f'Your name is: {username}')")

try:
    import msvcrt
except ImportError:
    import selectors
    import termios
    inputtimeout = _posix_inputtimeout
finally:
    import time
    inputtimeout = _win_inputtimeout
