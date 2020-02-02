# getkeys.py
# Citation: Box Of Hats (https://github.com/Box-Of-Hats )

import win32api as wapi
import win32gui
import time

keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'APS$/\\":
    keyList.append(char)


def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    mouse_click = []
    for click in [0x01, 0x02]:
        if wapi.GetAsyncKeyState(click):
            mouse_click.append(click)
    x, y = wapi.GetCursorPos()
    # print(flags, hcursor, (x, y))
    return keys, [[x, y], mouse_click]
