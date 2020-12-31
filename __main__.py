import os, time
import pyautogui
import pytesseract
import cv2
import numpy as np
from PIL import Image
from GameMechanic import AoE3Env, AoE3yBotAi
from Units import Unit, Units, Villager, Mill, TownCenter, Market, Wagon


class Bot(AoE3yBotAi):

    def onStart(self):
        print(len(self.GameEnv.InGameGui))

    def onStep(self):
        print(f"Age: {self.Age}, Iteration: {self.Iteration}")
        print(self.Food, self.Wood, self.Gold)

        # self.GameEnv.InGameGui["FoodCollectorsSlot"].show()
        # self.GameEnv.InGameGui["WoodCollectorsSlot"].show()
        # self.GameEnv.InGameGui["GoldCollectorsSlot"].show()
        self.GameEnv.InGameGui["AgeSlot"].show()
        # self.GameEnv.InGameGui["MenuButton"].show()
        # self.GameEnv.InGameGui["Map"].show()

        # if self.Iteration == 1:
        #     # construction of the first town
        #     time.sleep(Wagon.BuildTownCenter())
        #     time.sleep(30)
        #
        # elif self.Iteration == 2:
        #     idlv = self.GameEnv.selectIdleVillager()
        #     if idlv is not None:
        #         time.sleep(idlv.BuildMarket())
        #
        # elif self.Iteration == 3:
        #     [time.sleep(TownCenter.TrainVillager()) for _ in range(2)]
        #     time.sleep(30)
        #
        # elif self.Iteration == 4:
        #     time.sleep(self.GameEnv.getDeckCard("300Woods"))
        #
        # elif self.Iteration == 5:
        #     idlv = self.GameEnv.selectIdleVillager()
        #     time.sleep(idlv.BuildMill())
        #
        # elif self.Iteration == 6:
        #     while self.GameEnv.selectIdleVillager() is not None:
        #         Villager.WorkOnMill()
        #
        # elif self.Iteration >= 7:
        #     if self.Food >= 500 and self.Food >= 4*self.Gold:
        #         market = self.GameEnv.selectMarket()
        #         market.BuyGoldWithFood()
        # if self.GameEnv.selectIdleVillager() is not None:
        #     Villager.WorkOnMill()
        super(Bot, self).onStep()

    def onEnd(self):
        pass


if __name__ == '__main__':
    # run as admin -> https://stackoverflow.com/questions/19672352/how-to-run-python-script-with-elevated-privilege-on-windows
    # os.system("python OpenGame.py")
    # time.sleep(60)

    Jarex = Bot("Jarex", "British")
    gameEnv = AoE3Env(Jarex)
    gameEnv.run()

