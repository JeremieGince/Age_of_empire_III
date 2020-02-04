import os, time
import pyautogui
import pytesseract
import cv2
import numpy as np
from PIL import Image
from InGameGUIParser import IGameAoE3GUIParser

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class GameEnvironment:
    digitsNumber: set = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}

    def __init__(self, botInstance):
        self._iteration: int = 0
        self.InGameGui = IGameAoE3GUIParser()

        self._bot = botInstance
        self._bot.setGameEnv(self)

        self._food: int = 0
        self._wood: int = 0
        self._gold: int = 0
        self._hmVillager: int = 0

    @property
    def Food(self) -> int:
        return self._food

    @property
    def Wood(self) -> int:
        return self._wood

    @property
    def Gold(self) -> int:
        return self._gold

    @property
    def HmVillager(self) -> int:
        return self._hmVillager

    @property
    def Iteration(self) -> int:
        return self._iteration

    def updateFood(self):
        foodPos = pyautogui.locateOnScreen("Icons/Food.PNG", confidence=0.9, grayscale=True)
        foodText = pyautogui.screenshot(region=(foodPos[0] + foodPos[2], foodPos[1], foodPos[2] * 1.5, foodPos[3]))
        foodText = -cv2.cvtColor(np.array(foodText), cv2.COLOR_RGB2GRAY)
        text = pytesseract.image_to_string(Image.fromarray(foodText), config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
        # for digit in text:
        #     if digit not in GameEnvironment.digitsNumber:
        #         text.replace(digit, '')
        if text:
            try:
                self._food = int(float(text))
            except Exception:
                pass

    def updateWood(self):
        woodPos = pyautogui.locateOnScreen("Icons/Wood.PNG", confidence=0.9, grayscale=True)
        woodText = pyautogui.screenshot(region=(woodPos[0] + woodPos[2], woodPos[1], woodPos[2] * 1.5, woodPos[3]))
        woodText = -cv2.cvtColor(np.array(woodText), cv2.COLOR_RGB2GRAY)
        text = pytesseract.image_to_string(Image.fromarray(woodText), config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
        # for digit in text:
        #     if digit not in GameEnvironment.digitsNumber:
        #         text.replace(digit, '')
        if text:
            try:
                self._wood = int(float(text))
            except Exception:
                pass

    def updateGold(self):
        goldPos = pyautogui.locateOnScreen("Icons/Gold.PNG", confidence=0.9, grayscale=True)
        goldText = pyautogui.screenshot(region=(goldPos[0] + goldPos[2], goldPos[1], goldPos[2] * 1.5, goldPos[3]))
        goldText = -cv2.cvtColor(np.array(goldText), cv2.COLOR_RGB2GRAY)
        text = pytesseract.image_to_string(Image.fromarray(goldText), config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
        # for digit in text:
        #     if digit not in GameEnvironment.digitsNumber:
        #         text.replace(digit, '')
        if text:
            try:
                self._gold = int(float(text))
            except Exception:
                pass
        cv2.imshow("dodu", np.array(goldText))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def updateHmVillager(self):
        resourcePos = pyautogui.locateOnScreen(f"Icons/Villagers.PNG", confidence=0.9, grayscale=True)
        resourceText = pyautogui.screenshot(region=(resourcePos[0] + resourcePos[2], resourcePos[1], resourcePos[2] * 1.5, resourcePos[3]))
        resourceText = -cv2.cvtColor(np.array(resourceText), cv2.COLOR_RGB2GRAY)
        text = pytesseract.image_to_string(Image.fromarray(resourceText), config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
        for digit in text:
            if digit not in GameEnvironment.digitsNumber:
                text.replace(digit, '')
        if text:
            try:
                self._hmVillager = int(float(text))
            except Exception:
                pass
        # cv2.imshow("dodu", np.array(resourceText))
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()

    def updateResource(self, resourceName: str):
        resourcePos = pyautogui.locateOnScreen(f"Icons/{resourceName}.PNG", confidence=0.9, grayscale=True)
        resourceText = pyautogui.screenshot(region=(resourcePos[0] + resourcePos[2], resourcePos[1], resourcePos[2] * 1.5, resourcePos[3]))
        resourceText = -cv2.cvtColor(np.array(resourceText), cv2.COLOR_RGB2GRAY)
        text = pytesseract.image_to_string(Image.fromarray(resourceText))
        for digit in text:
            if digit not in GameEnvironment.digitsNumber:
                text.replace(digit, '')
        if text:
            try:
                self._food = int(float(text))
            except Exception:
                pass
        cv2.imshow("dodu", np.array(resourceText))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def updateResources(self):
        self.updateFood()
        self.updateWood()
        self.updateGold()
        self.updateHmVillager()
        print(f"Food: {self.Food}, Wood: {self.Wood}, Gold: {self.Gold}, HmVillager: {self.HmVillager}")

    def run(self):
        self._bot.onStart()
        time.sleep(5)
        while self.Iteration <= 1_000:
            print(f"iteration: {self.Iteration}")
            try:
                self.updateResources()
            except TypeError as err:
                print(err)

            self._bot.onStep()

            self._iteration += 1
        self._bot.onEnd()


GameEnv = GameEnvironment


class BotAi:
    def __init__(self, name: str):
        self.GameEnv = None
        self.name: str = name

    @property
    def Food(self) -> int:
        return self.GameEnv.Food

    @property
    def Wood(self) -> int:
        return self.GameEnv.Wood

    @property
    def Gold(self) -> int:
        return self.GameEnv.Gold

    @property
    def HmVillager(self) -> int:
        return self.GameEnv.HmVillager

    @property
    def Iteration(self) -> int:
        return self.GameEnv.Iteration

    def setGameEnv(self, gameEnv):
        self.GameEnv: GameEnv = gameEnv

    def onStart(self):
        raise NotImplementedError()

    def onStep(self):
        raise NotImplementedError()

    def onEnd(self):
        raise NotImplementedError()


if __name__ == '__main__':
    pass

