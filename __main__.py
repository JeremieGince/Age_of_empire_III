import os, time
import pyautogui
import pytesseract
import cv2
import numpy as np
from PIL import Image
from GameMechanic import GameEnv, BotAi


class Bot(BotAi):
    def onStart(self):
        pass

    def onStep(self):
        pass

    def onEnd(self):
        pass


if __name__ == '__main__':
    # run as admin -> https://stackoverflow.com/questions/19672352/how-to-run-python-script-with-elevated-privilege-on-windows
    os.system("python OpenGame.py")
    # time.sleep(60)
    time.sleep(1)

    # icon_pos = pyautogui.locateOnScreen("Buttons/Play.PNG")
    # print("icon pos: ", (icon_pos[0], icon_pos[1]))
    # pyautogui.moveTo(icon_pos[0]+10, icon_pos[1]+10)
    # time.sleep(1)
    # pyautogui.leftClick(icon_pos[0]+10, icon_pos[1]+10)

    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # while True:
    #     foodPos = pyautogui.locateOnScreen("Icons/Food.PNG")
    #     print(f"FoodPos: {foodPos}")
    #     foodText = pyautogui.screenshot(region=(foodPos[0]+foodPos[2], foodPos[1], foodPos[2]*1.5, foodPos[3]))
    #     foodText = -cv2.cvtColor(np.array(foodText), cv2.COLOR_RGB2GRAY)
    #     text = pytesseract.image_to_string(Image.fromarray(foodText))
    #     print(f"text: {text}")
    #     cv2.imshow("dodu", np.array(foodText))
    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #         cv2.destroyAllWindows()
    #         break

    Jarex = Bot("Jarex")
    gameEnv = GameEnv(Jarex)
    gameEnv.run()

