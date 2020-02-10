import pyautogui
import time

tempGroup = 9

HandleToHotKeys: dict = {
    # Game world Hotkeys
    "Move Camera Left": ["left"],
    "Move Camera Right": ["right"],
    "Move Camera Forward": ["up"],
    "Move Camera Backward": ["down"],

    # Find Unit Hotkeys
    "Find idle Villager": ["."],
    "Find Explorer": ["é"],
    "Find idle Military": [","],
    "Find Home City": ["h"],
    "Find Town Center": ["t"],
    "Find Wagon": [";"],
    "Find Mill": ["CTRL", "i"],
    "Find Market": ["CTRL", "m"],

    # Building Construction Hotkeys
    "Build Town Center": ["g"],
    "Build Market": ["m"],
    "Build Mill": ["i"],

    # Selection Group Hotkeys
    "Select temp Group": [str(tempGroup)],
    "Create temp Group": ["CTRL", str(tempGroup)],
    "Create Group 9": ["CTRL", "9"],

    # Town Center Hotkeys
    "Train Villager": ["v"],
}


def sleepKeys(func):
    time.sleep(0.1)
    re = func
    time.sleep(0.7)
    return re


@sleepKeys
def SendHotKeys(handle: str):
    assert handle in HandleToHotKeys
    pyautogui.hotkey(*HandleToHotKeys[handle])


@sleepKeys
def Find_idle_Villager():
    pyautogui.hotkey(*HandleToHotKeys["Find idle Villager"])




