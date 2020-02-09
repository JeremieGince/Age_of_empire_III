import cv2
import os
import Hotkeys
import pyautogui
from GUIParser import GUIParser


class Unit:
    UnitIconsDirectory: str = fr"{os.getcwd()}/UnitIcons/"

    def __init__(self, name: str, IconPath: str, GameGui: GUIParser):
        self.name = name
        self.IconPath = IconPath
        self.GameGui = GameGui

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
    def __init__(self, IconPath: str, GameGui: GUIParser):
        super(Wagon, self).__init__("Wagon", IconPath, GameGui)

    @staticmethod
    def BuildTownCenter():
        Hotkeys.SendHotKeys("Find Wagon")
        Hotkeys.SendHotKeys("Build Town Center")
        center = pyautogui.size()[0]//2, pyautogui.size()[1]//2
        pyautogui.leftClick(*center)
        return 30


class TownCenter(Unit):
    def __init__(self, IconPath: str, GameGui: GUIParser):
        super(TownCenter, self).__init__("TownCenter", IconPath, GameGui)

    @staticmethod
    def TrainVillager():
        Hotkeys.SendHotKeys("Find Town Center")
        Hotkeys.SendHotKeys("Train Villager")
        return 1


class Villager(Unit):
    def __init__(self, IconPath: str, GameGui: GUIParser):
        super(Villager, self).__init__("Villager", IconPath, GameGui)

    @staticmethod
    def BuildMarket():
        Hotkeys.SendHotKeys("Build Market")
        pyautogui.leftClick()
        return 30  # elapse time tu build [s]

    @staticmethod
    def BuildMill():
        # TODO: Make a new Class Builder to construct new building
        Hotkeys.SendHotKeys("Build Mill")
        pyautogui.leftClick()  # may add several clicks to a random variance location
        return 30  # elapse time tu build [s]

    @staticmethod
    def WorkOnMill():
        Hotkeys.SendHotKeys("Find idle Villager")
        Hotkeys.SendHotKeys("Create temp Group")
        Hotkeys.SendHotKeys("Find Mill")
        Hotkeys.SendHotKeys("Select temp Group")
        pyautogui.rightClick(pyautogui.size()[0]//2, pyautogui.size()[1]//2)


class Market(Unit):
    def __init__(self, IconPath: str, GameGui: GUIParser):
        super(Market, self).__init__("Market", IconPath, GameGui)

    def BuyFoodWithGold(self):
        Hotkeys.SendHotKeys("Find Market")
        self.GameGui["OptionSlot6"].click()

    def BuyWoodWithGold(self):
        Hotkeys.SendHotKeys("Find Market")
        self.GameGui["OptionSlot7"].click()

    def BuyGoldWithFood(self):
        Hotkeys.SendHotKeys("Find Market")
        self.GameGui["OptionSlot12"].click()

    def BuyGoldWithWood(self):
        Hotkeys.SendHotKeys("Find Market")
        self.GameGui["OptionSlot13"].click()


class Mill(Unit):
    def __init__(self, IconPath: str, GameGui: GUIParser):
        super(Mill, self).__init__("Mill", IconPath, GameGui)

    def Improve(self):
        Hotkeys.SendHotKeys("Find Mill")
        self.GameGui["OptionSlot0"].click()


if __name__ == '__main__':
    pass
