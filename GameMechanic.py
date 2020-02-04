import os, time
from GUIParser import InGameAoE3GUIParser


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
        self._bot.onStart()
        time.sleep(5)
        while self.Iteration <= 1_000:
            print(f"iteration: {self.Iteration}")
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
            self._food = int(woodStr)
            self.GuiItems_updates["WoodSlot"] = self.Iteration

    def updateGoldSlot(self):
        hmVillagerStr = repr(self.InGameGui["GoldSlot"])
        # self.InGameGui["GoldSlot"].show()
        if hmVillagerStr:
            self._food = int(hmVillagerStr)
            self.GuiItems_updates["GoldSlot"] = self.Iteration

    def updateHmVillagerSlot(self):
        hmVillagerStr = repr(self.InGameGui["HmIdleVillagerSlot"])
        # self.InGameGui["HmIdleVillagerSlot"].show()
        if hmVillagerStr:
            self._food = int(hmVillagerStr)
            self.GuiItems_updates["HmIdleVillagerSlot"] = self.Iteration


AoE3Env = AoE3Environment


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

