import subprocess
import pyautogui
import time
import sys

try:
    folder_path = sys.argv[1]
except IndexError:
    folder_path = "."

with open("{}/GamePath.txt".format(folder_path), 'r') as fich:
    game_path = fich.readline()

subprocess.call([game_path], shell=True)
# subprocess.Popen([game_path], stdout=subprocess.PIPE)
time.sleep(20)
# icon_pos = pyautogui.locateOnScreen("{}/AgeIcon.PNG".format(folder_path))
# print("icon pos: ", (icon_pos[0], icon_pos[1]))
# pyautogui.moveTo(icon_pos[0], icon_pos[1])
# pyautogui.dragTo(0, 0)
print("Done")
