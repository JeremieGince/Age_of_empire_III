import cv2
import os
import Hotkeys
import pyautogui
from GUIParser import GUIParser
from GameMechanic import GameEnv, AoE3Env


class Unit:
    UnitIconsDirectory: str = fr"{os.getcwd()}/UnitIcons/"

    def __init__(self, name: str, IconPath: str, gameEnv: GameEnv):
        self.name = name
        self.IconPath = IconPath
        self.gameEnv = gameEnv

    @property
    def img(self):
        return cv2.imread(self.IconPath)

    def show(self):
        cv2.imshow(self.name, self.img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()


class Units(list):
    def __init__(self, iterable):
        super(Units, self).__init__()
        for unit in iterable:
            assert isinstance(unit, Unit)
            self.append(unit)


class Wagon(Unit):
    def __init__(self, IconPath: str, gameEnv: GameEnv):
        super(Wagon, self).__init__("Wagon", IconPath, gameEnv)

    @staticmethod
    def BuildTownCenter():
        Hotkeys.SendHotKeys("Find Wagon")
        Hotkeys.SendHotKeys("Build Town Center")
        AoE3Env.build()
        return 30


class TownCenter(Unit):
    def __init__(self, IconPath: str, gameEnv: GameEnv):
        super(TownCenter, self).__init__("TownCenter", IconPath, gameEnv)

    @staticmethod
    def TrainVillager():
        Hotkeys.SendHotKeys("Find Town Center")
        Hotkeys.SendHotKeys("Train Villager")
        return 1


class Villager(Unit):
    def __init__(self, IconPath: str, gameEnv: GameEnv):
        super(Villager, self).__init__("Villager", IconPath, gameEnv)

    @staticmethod
    def BuildMarket():
        Hotkeys.SendHotKeys("Build Market")
        AoE3Env.build()
        return 30  # elapse time tu build [s]

    @staticmethod
    def BuildMill():
        Hotkeys.SendHotKeys("Build Mill")
        AoE3Env.build()
        return 30  # elapse time tu build [s]

    @staticmethod
    def WorkOnMill():
        Hotkeys.SendHotKeys("Find idle Villager")
        Hotkeys.SendHotKeys("Create temp Group")
        Hotkeys.SendHotKeys("Find Mill")
        Hotkeys.SendHotKeys("Select temp Group")
        AoE3Env.madeCrossSearch(["GameMessages/Mill_Food_building.PNG"], func=pyautogui.rightClick)
        pyautogui.hotkey("esc")


class Market(Unit):
    def __init__(self, IconPath: str, gameEnv: GameEnv):
        super(Market, self).__init__("Market", IconPath, gameEnv)

    def BuyFoodWithGold(self):
        Hotkeys.SendHotKeys("Find Market")
        self.gameEnv.InGameGui["OptionSlot6"].click()

    def BuyWoodWithGold(self):
        Hotkeys.SendHotKeys("Find Market")
        self.gameEnv.InGameGui["OptionSlot7"].click()

    def BuyGoldWithFood(self):
        Hotkeys.SendHotKeys("Find Market")
        self.gameEnv.InGameGui["OptionSlot12"].click()

    def BuyGoldWithWood(self):
        Hotkeys.SendHotKeys("Find Market")
        self.gameEnv.InGameGui["OptionSlot13"].click()


class Mill(Unit):
    def __init__(self, IconPath: str, gameEnv: GameEnv):
        super(Mill, self).__init__("Mill", IconPath, gameEnv)

    def Improve(self):
        Hotkeys.SendHotKeys("Find Mill")
        self.gameEnv.InGameGui["OptionSlot0"].click()


if __name__ == '__main__':
    pass
