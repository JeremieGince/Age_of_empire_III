import os, time
import pyautogui
import pytesseract
import cv2
import numpy as np
from PIL import Image
from GameMechanic import AoE3Env, BotAi


class Bot(BotAi):
    def onStart(self):
        pass

    def onStep(self):
        print(f"Food: {self.Food}")

    def onEnd(self):
        pass


if __name__ == '__main__':
    # run as admin -> https://stackoverflow.com/questions/19672352/how-to-run-python-script-with-elevated-privilege-on-windows
    # os.system("python OpenGame.py")
    # time.sleep(60)
    time.sleep(1)

    Jarex = Bot("Jarex")
    gameEnv = AoE3Env(Jarex)
    gameEnv.run()

