import os, time
from GUIParser import InGameAoE3GUIParser, GuiItem
import Hotkeys
import pyautogui
import util


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

    ResourceToUpgradeAge: dict = {
        1: {
            "Food": 800,
            "Wood": 0,
            "Gold": 0
        },

        2: {
            "Food": 1_200,
            "Wood": 0,
            "Gold": 1_000
        },

        3: {
            "Food": 2_000,
            "Wood": 0,
            "Gold": 1_200
        },

        4: {
            "Food": 4_000,
            "Wood": 0,
            "Gold": 4_000
        },
    }

    def __init__(self, botInstance):
        super(AoE3Environment, self).__init__(botInstance)
        self.InGameGui = InGameAoE3GUIParser()

        self.GuiItems_updates: dict = {name: -1 for name, _ in self.InGameGui.items()}

        self._Age: int = 0

        self._food: int = 0
        self._wood: int = 0
        self._gold: int = 0
        self._hmVillager: int = 0

        self._foodCollectors: int = 0
        self._woodCollectors: int = 0
        self._goldCollectors: int = 0
        self._hmIdleVillager: int = 0

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
        if self.GuiItems_updates["HmVillagerSlot"] < self.Iteration:
            self.updateHmVillagerSlot()
        return self._hmVillager

    @property
    def FoodCollectors(self) -> int:
        if self.GuiItems_updates["FoodCollectorsSlot"] < self.Iteration:
            self.updateFoodCollectorsSlot()
        return self._foodCollectors

    @property
    def WoodCollectors(self) -> int:
        if self.GuiItems_updates["WoodCollectorsSlot"] < self.Iteration:
            self.updateWoodCollectorsSlot()
        return self._woodCollectors

    @property
    def GoldCollectors(self) -> int:
        if self.GuiItems_updates["GoldCollectorsSlot"] < self.Iteration:
            self.updateGoldCollectorsSlot()
        return self._goldCollectors

    @property
    def HmIdleVillager(self) -> int:
        if self.GuiItems_updates["HmIdleVillagerSlot"] < self.Iteration:
            self.updateHmIdleVillagerSlot()
        return self._hmIdleVillager

    @property
    def Age(self) -> int:
        if self.GuiItems_updates["AgeSlot"] < self.Iteration:
            self.updateAgeSlot()
        return self._Age

    def updateAgeSlot(self):
        AgeByPath: dict = {
            1: "GameMessages/1_Discovery_Age.PNG",
            2: "GameMessages/2_Colonial_Age.png",
            3: "GameMessages/3_Fortress_Age.png",
            4: "GameMessages/4_Industrial_Age.png",
            5: "GameMessages/5_Imperial_Age.png"
        }
        for age, path in AgeByPath.items():
            if self.InGameGui.imgIn(path):
                self._Age = age
                print(f"age: {age}")
                break

        self.GuiItems_updates["AgeSlot"] = self.Iteration

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
        hmVillagerStr = repr(self.InGameGui["HmVillagerSlot"])
        # self.InGameGui["HmVillagerSlot"].show()
        if hmVillagerStr:
            self._hmVillager = int(hmVillagerStr)
            self.GuiItems_updates["HmVillagerSlot"] = self.Iteration

    def updateFoodCollectorsSlot(self):
        foodCollectorsStr = repr(self.InGameGui["FoodCollectorsSlot"])
        if foodCollectorsStr:
            self._foodCollectors = int(foodCollectorsStr)
            self.GuiItems_updates["FoodCollectorsSlot"] = self.Iteration

    def updateWoodCollectorsSlot(self):
        woodCollectorsStr = repr(self.InGameGui["WoodCollectorsSlot"])
        if woodCollectorsStr:
            self._woodCollectors = int(woodCollectorsStr)
            self.GuiItems_updates["WoodCollectorsSlot"] = self.Iteration

    def updateGoldCollectorsSlot(self):
        foodCollectorsStr = repr(self.InGameGui["GoldCollectorsSlot"])
        if foodCollectorsStr:
            self._goldCollectors = int(foodCollectorsStr)
            self.GuiItems_updates["GoldCollectorsSlot"] = self.Iteration

    def updateHmIdleVillagerSlot(self):
        HmIdleVillagerSlotStr = repr(self.InGameGui["HmIdleVillagerSlot"])
        if HmIdleVillagerSlotStr:
            self._hmIdleVillager = int(HmIdleVillagerSlotStr)
            self.GuiItems_updates["HmIdleVillagerSlot"] = self.Iteration

    def getDeckCard(self, CardName: str):
        Hotkeys.SendHotKeys("Find Home City")
        if CardName not in self.InGameGui.items():
            try:
                self.InGameGui.addItem(GuiItem(f"{CardName}", None, IconPath=os.getcwd()+f"/DeckCards/{CardName}.PNG"))
            except TypeError:
                time.sleep(1)
                self.InGameGui.addItem(GuiItem(f"{CardName}", None, IconPath=os.getcwd()+f"/DeckCards/{CardName}.PNG"))

        card = self.InGameGui[CardName]
        card.click()
        pyautogui.hotkey("esc")
        return 60

    def selectFoodCollector(self):
        from Units import Unit, Villager
        self.InGameGui["FoodCollectorsSlot"].click()
        unitIcon = Unit.UnitIconsDirectory + self._bot.civ + "/Villager.PNG"
        return Villager(unitIcon, self) if self.InGameGui.imgIn(unitIcon) else None

    def selectWoodCollector(self):
        self.InGameGui["WoodCollectorsSlot"].click()

    def selectGoldCollector(self):
        self.InGameGui["GoldCollectorsSlot"].click()

    def selectIdleVillager(self):
        from Units import Unit, Villager
        Hotkeys.Find_idle_Villager()
        unitIcon = Unit.UnitIconsDirectory+self._bot.civ+"/Villager.PNG"
        return Villager(unitIcon, self) if self.InGameGui.imgIn(unitIcon) else None

    def selectMarket(self):
        from Units import Unit, Market
        Hotkeys.SendHotKeys("Find Market")
        unitIcon = Unit.UnitIconsDirectory+self._bot.civ+"/Market.PNG"
        return Market(unitIcon, self) if self.InGameGui.imgIn(unitIcon) else None

    def selectMill(self):
        from Units import Unit, Mill
        Hotkeys.SendHotKeys("Find Mill")
        unitIcon = Unit.UnitIconsDirectory + self._bot.civ + "/Mill.PNG"
        return Mill(unitIcon, self) if self.InGameGui.imgIn(unitIcon) else None

    def selectTownCenter(self):
        from Units import Unit, TownCenter
        Hotkeys.SendHotKeys("Find Town Center")
        unitIcon = Unit.UnitIconsDirectory + self._bot.civ + "/TownCenter.png"
        return TownCenter(unitIcon, self) if self.InGameGui.imgIn(unitIcon) else None

    def selectHero(self):
        return

    @staticmethod
    def build():
        from GUIParser import GUIParser
        center = pyautogui.size()[0] // 2, pyautogui.size()[1] // 2
        # center = self.InGameGui.activeWindow.center
        pyautogui.moveTo(*center)
        errorMess_paths = [fr"GameMessages/Other_objects_prevent_you_from_placing_this_here.PNG",
                           fr"GameMessages/You_must_explore_this_area_before_placing_items_there.PNG",
                           fr"GameMessages/This_building_has_corps_around_it_You_need_to_allow_more_space.PNG",
                           fr"GameMessages/You_may_not_obstruct_a_Trade_Route.PNG"]

        search = AoE3Env.PerformCrossSearch(errorMess_paths, func=pyautogui.leftClick, sleep=0.7, inv=True)
        if search is not None:
            return None

        while any([GUIParser.imgIn(mess) for mess in errorMess_paths]):
            direction: str = util.randomDirection(("left", "right", "up", "down"))
            pyautogui.keyDown(direction)
            util.randomSleep(b=0.2)
            pyautogui.keyUp(direction)
            pyautogui.press(direction)

        pyautogui.leftClick()
        pyautogui.hotkey("esc")

    @staticmethod
    def PerformCrossSearch(pathsToFind: list, variances: tuple = (50, 100, 150), func=pyautogui.rightClick,
                           sleep: float = 1.0, **kwargs):
        """
        Perform a cross search to find the given paths in the screen.
        :param pathsToFind: The path we want to find. (list[str])
        :param variances: The variances points (tuple[int])
        :param func: The function to perform when a path is find.
        :param sleep: The time to sleep between each point [s] (float)
        :param kwargs:
                        :inv: To perform a invert search. i.e We don't want to see any of the path.
        :return: The found position (int, int) if found else None
        """
        import time
        from GUIParser import GUIParser

        inv: bool = kwargs.get("inv", False)

        center = pyautogui.size()[0] // 2, pyautogui.size()[1] // 2
        pyautogui.moveTo(*center)
        searchPositions: list = list()
        for var in variances:
            searchPositions.extend([(center[0], center[1]+var),
                                    (center[0]+var, center[1]),
                                    (center[0], center[1]-var),
                                    (center[0]-var, center[1])])

        for searchPos in searchPositions:
            pyautogui.moveTo(searchPos)
            time.sleep(sleep)
            if inv:
                if not any([GUIParser.imgIn(path) for path in pathsToFind]):
                    func()
                    pyautogui.hotkey("esc")
                    return searchPos
            else:
                if any([GUIParser.imgIn(path) for path in pathsToFind]):
                    func()
                    pyautogui.hotkey("esc")
                    return searchPos
        return None

    @staticmethod
    def deselectAll():
        pyautogui.hotkey("esc")

    def findSilverMine(self):
        region = self.InGameGui.locate("MapItems/SilverMineTiny.png",
                                       grayscale=False, region=self.InGameGui["Map"].box,
                                       confidence=0.5)
        if region is not None:
            SilverMine = GuiItem("SilverMineMapItem", region=region, IconPath="MapItems/SilverMineTiny.png")
            self.InGameGui.addItem(SilverMine)
            SilverMine.click()
        return region


GameEnv = GameEnvironment
AoE3Env = AoE3Environment


class BotAi:
    def __init__(self, name: str, civ: str):
        self.GameEnv = None
        self._name: str = name
        self._civ: str = civ

    @property
    def name(self) -> str:
        return self._name

    @property
    def civ(self) -> str:
        return self._civ

    @property
    def Age(self) -> int:
        return self.GameEnv.Age

    def setGameEnv(self, gameEnv):
        self.GameEnv: GameEnv = gameEnv

    def onStart(self):
        raise NotImplementedError()

    def onStep(self):
        raise NotImplementedError()

    def onEnd(self):
        raise NotImplementedError()


class AoE3yBotAi(BotAi):
    CollectorsRatioByAge: dict = {
        1: {
            "Food": 0.4,
            "Wood": 0.5,
            "Gold": 0.1
        },

        2: {
            "Food": 0.5,
            "Wood": 0.3,
            "Gold": 0.2
        },

        3: {
            "Food": 0.5,
            "Wood": 0.3,
            "Gold": 0.2
        },

        4: {
            "Food": 0.5,
            "Wood": 0.3,
            "Gold": 0.2
        },

        5: {
            "Food": 0.5,
            "Wood": 0.1,
            "Gold": 0.4
        },
    }

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

    @property
    def FoodCollectors(self) -> int:
        return self.GameEnv.FoodCollectors

    @property
    def WoodCollectors(self) -> int:
        return self.GameEnv.WoodCollectors

    @property
    def GoldCollectors(self) -> int:
        return self.GameEnv.GoldCollectors

    @property
    def HmIdleVillager(self) -> int:
        return self.GameEnv.HmIdleVillager

    def distributeWorkers(self):
        from Units import Villager
        HmIdealWorkersByResource: dict = {
            resource: self.CollectorsRatioByAge[self.Age][resource]*self.HmVillager
            for resource in {"Food", "Wood", "Gold"}
        }

        HmCurrentWorkersByResource: dict = {
            "Food": self.FoodCollectors,
            "Wood": self.WoodCollectors,
            "Gold": self.GoldCollectors
        }

        DeltaWorkersByResource: dict = {
            resource: HmIdealWorkersByResource[resource] - HmCurrentWorkersByResource[resource]
            for resource in {"Food", "Wood", "Gold"}
        }

        idleVillager = self.GameEnv.selectIdleVillager()
        if idleVillager is not None:
            idleVillager.WorkOnSilverMine()

        idleVillager = self.GameEnv.selectIdleVillager()
        if idleVillager is not None:
            idleVillager.WorkOnMill()

        print(HmIdealWorkersByResource, HmCurrentWorkersByResource, DeltaWorkersByResource, sep='\n')
        if self.GoldCollectors < HmIdealWorkersByResource["Gold"] and self.FoodCollectors > HmIdealWorkersByResource["Food"]:
            villager = self.GameEnv.selectFoodCollector()
            if villager is not None:
                print(f"{villager} -> {villager.WorkOnSilverMine}")
                villager.WorkOnSilverMine()

    def CanImproveAge(self):
        resources = AoE3Env.ResourceToUpgradeAge[self.Age]
        print(resources, all([self.Food >= resources["Food"], self.Wood >= resources["Wood"], self.Gold >= resources["Gold"]]))
        return all([self.Food >= resources["Food"], self.Wood >= resources["Wood"], self.Gold >= resources["Gold"]])

    def ImproveAge(self):
        tc = self.GameEnv.selectTownCenter()
        if tc is not None and self.CanImproveAge():
            tc.ImproveAge()

    def onStart(self):
        pass

    def onStep(self):
        from Units import Wagon, TownCenter
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
        #     if idlv is not None:
        #         time.sleep(idlv.BuildMill())
        #
        # else:
        #     self.distributeWorkers()
        #     self.ImproveAge()

        self.distributeWorkers()
        self.ImproveAge()

    def onEnd(self):
        pass


if __name__ == '__main__':
    pass

