import pyautogui
from Units import Unit, Units


def Find_idle_Villager():
    pyautogui.hotkey(".")
    return Unit("Villager", "")

