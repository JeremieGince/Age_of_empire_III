import os, time
import pyautogui
import pytesseract
import cv2
import numpy as np
from PIL import Image
from GameMechanic import AoE3Env, BotAi
from Units import *


class Bot(BotAi):
    def onStart(self):
        print(len(self.GameEnv.InGameGui))
        # idlv = self.GameEnv.selectIdleVillager()
        # if self.GameEnv.selectMarket() is None:
        #     idlv.BuildMarket()

    def onStep(self):
        print(f"iteration: {self.Iteration}")
        print(self.Food, self.Wood, self.Gold)
        # for i in range(4):
        #     market = self.GameEnv.selectMarket()
        #     if self.Gold > 200:
        #         market.BuyWoodWithGold()
        #     if self.Food > 100:
        #         market.BuyGoldWithFood()

        if self.Iteration == 1:
            # construction of the first town
            time.sleep(Wagon.BuildTownCenter())
            time.sleep(30)

        elif self.Iteration == 2:
            idlv = self.GameEnv.selectIdleVillager()
            time.sleep(idlv.BuildMarket())

        elif self.Iteration == 3:
            [time.sleep(TownCenter.TrainVillager()) for _ in range(2)]
            time.sleep(30)

        elif self.Iteration == 4:
            time.sleep(self.GameEnv.getDeckCard("300Woods"))

        elif self.Iteration == 5:
            idlv = self.GameEnv.selectIdleVillager()
            time.sleep(idlv.BuildMill())

        elif self.Iteration == 6:
            while self.GameEnv.selectIdleVillager() is not None:
                Villager.WorkOnMill()

        elif self.Iteration >= 7:
            if self.Food >= 500 and self.Food >= 4*self.Gold:
                market = self.GameEnv.selectMarket()
                market.BuyGoldWithFood()

    def onEnd(self):
        pass


if __name__ == '__main__':
    # run as admin -> https://stackoverflow.com/questions/19672352/how-to-run-python-script-with-elevated-privilege-on-windows
    # os.system("python OpenGame.py")
    # time.sleep(60)
    # time.sleep(1)

    Jarex = Bot("Jarex", "British")
    gameEnv = AoE3Env(Jarex)
    gameEnv.run()

