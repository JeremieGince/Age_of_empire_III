import os, time
from GUIParser import InGameAoE3GUIParser, GuiItem
import Hotkeys
from Units import *


class GameEnvironment:
    def __init__(self, botInstance):
        self._iteration: int = 0

        self._bot = botInstance
        self._bot.setGameEnv(self)

        self.InGameGui = None

    @property
    def Iteration(self) -> int:
        return self._iteration

    def run(self):
        time.sleep(3)
        self._bot.onStart()
        while self.Iteration <= 1_000:
            self._bot.onStep()

            self._iteration += 1
        self._bot.onEnd()


class AoE3Environment(GameEnvironment):
    def __init__(self, botInstance):
        super(AoE3Environment, self).__init__(botInstance)
        self.InGameGui = InGameAoE3GUIParser()

        self.GuiItems_updates: dict = {name: 0 for name, _ in self.InGameGui.items()}

        self._food: int = 0
        self._wood: int = 0
        self._gold: int = 0
        self._hmVillager: int = 0

    @property
    def Food(self) -> int:
        if self.GuiItems_updates["FoodSlot"] < self.Iteration:
            self.updateFoodSlot()
        return self._food

    @property
    def Wood(self) -> int:
        if self.GuiItems_updates["WoodSlot"] < self.Iteration:
            self.updateWoodSlot()
        return self._wood

    @property
    def Gold(self) -> int:
        if self.GuiItems_updates["GoldSlot"] < self.Iteration:
            self.updateGoldSlot()
        return self._gold

    @property
    def HmVillager(self) -> int:
        if self.GuiItems_updates["HmIdleVillagerSlot"] < self.Iteration:
            self.updateFoodSlot()
        return self._hmVillager

    def updateFoodSlot(self):
        foodStr = repr(self.InGameGui["FoodSlot"])
        # self.InGameGui["FoodSlot"].show()
        if foodStr:
            self._food = int(foodStr)
            self.GuiItems_updates["FoodSlot"] = self.Iteration

    def updateWoodSlot(self):
        woodStr = repr(self.InGameGui["WoodSlot"])
        # self.InGameGui["WoodSlot"].show()
        if woodStr:
            self._wood = int(woodStr)
            self.GuiItems_updates["WoodSlot"] = self.Iteration

    def updateGoldSlot(self):
        goldStr = repr(self.InGameGui["GoldSlot"])
        # self.InGameGui["GoldSlot"].show()
        if goldStr:
            self._gold = int(goldStr)
            self.GuiItems_updates["GoldSlot"] = self.Iteration

    def updateHmVillagerSlot(self):
        hmVillagerStr = repr(self.InGameGui["HmIdleVillagerSlot"])
        # self.InGameGui["HmIdleVillagerSlot"].show()
        if hmVillagerStr:
            self._hmVillager = int(hmVillagerStr)
            self.GuiItems_updates["HmIdleVillagerSlot"] = self.Iteration

    def getDeckCard(self, CardName: str):
        Hotkeys.SendHotKeys("Find Home City")
        if CardName not in self.InGameGui.items():
            self.InGameGui.addItem(GuiItem(f"{CardName}", None, IconPath=os.getcwd()+f"/DeckCards/{CardName}.PNG"))

        card = self.InGameGui[CardName]
        card.click()
        return 60

    def selectIdleVillager(self):
        Hotkeys.Find_idle_Villager()
        unitIcon = Unit.UnitIconsDirectory+self._bot.civ+"/Villager.PNG"
        return Villager(unitIcon, self.InGameGui) if self.InGameGui.imgIn(unitIcon) else None

    def selectMarket(self):
        Hotkeys.SendHotKeys("Find Market")
        unitIcon = Unit.UnitIconsDirectory+self._bot.civ+"/Market.PNG"
        return Market(unitIcon, self.InGameGui) if self.InGameGui.imgIn(unitIcon) else None

    def selectMill(self):
        Hotkeys.SendHotKeys("Find Mill")
        unitIcon = Unit.UnitIconsDirectory + self._bot.civ + "/Mill.PNG"
        return Mill(unitIcon, self.InGameGui) if self.InGameGui.imgIn(unitIcon) else None


GameEnv = GameEnvironment
AoE3Env = AoE3Environment


class BotAi:
    def __init__(self, name: str, civ: str):
        self.GameEnv = None
        self.name: str = name
        self.civ: str = civ

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

