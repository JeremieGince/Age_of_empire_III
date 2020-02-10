import pyautogui
import os
import cv2
import numpy as np
from PIL import Image
import pytesseract
import time
import util


class GuiItem:
    def __init__(self, name: str, region: tuple, **kwargs):
        self.name: str = name

        if region is None:
            assert "IconPath" in kwargs
            region = pyautogui.locateOnScreen(kwargs.get("IconPath"), confidence=0.9, grayscale=True)
        assert len(region) == 4
        self.region: tuple = region  # (left, top, width, height)

        self.char_whitelist = kwargs.get("char_whitelist")
        self.iconPath = kwargs.get("IconPath")

    @property
    def box(self) -> tuple:
        """
        :return: (left, top, width, height)
        """
        return self.region

    @property
    def center(self) -> tuple:
        """
        Property -> Center position of the current Gui item
        :return: (x, y)
        """
        return self.box[0] + self.box[2]/2, self.box[1] + self.box[3]/2

    @property
    def img(self):
        return pyautogui.screenshot(region=self.box)

    def __repr__(self):
        gray = -cv2.cvtColor(np.array(self.img), cv2.COLOR_RGB2GRAY)
        threshold = util.thresholding(gray)
        if self.char_whitelist is not None:
            this = pytesseract.image_to_string(Image.fromarray(threshold),
                                               config=f'--psm 13 --oem 3 -c tessedit_char_whitelist={self.char_whitelist}')
        else:
            this = pytesseract.image_to_string(Image.fromarray(threshold))
        return this

    def show(self):
        gray = -cv2.cvtColor(np.array(self.img), cv2.COLOR_RGB2GRAY)
        threshold = util.thresholding(gray)
        cv2.imshow(self.name, np.array(threshold))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def click(self):
        """
        Perform a click on the Gui item
        :return: None
        """
        x, y = self.center
        pyautogui.click(x, y)


class GUIParser:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        self.GuiItems: dict = dict()
        self.setGuiItems()

        # https://automatetheboringstuff.com/2e/chapter20/
        self.activeWindow = pyautogui.getActiveWindow()

    def setGuiItems(self):
        raise NotImplementedError()

    def addItem(self, item: GuiItem):
        self.GuiItems[item.name] = item

    def __getitem__(self, itemName: str):
        return self.GuiItems[itemName]

    def getItem(self, itemName: str):
        return self.GuiItems[itemName]

    def getItemBox(self, itemName: str):
        return self.GuiItems[itemName].box

    def getItemRegion(self, itemName: str):
        return self.GuiItems[itemName].box

    def getItemCenter(self, itemName: str):
        return self.GuiItems[itemName].center

    def items(self):
        return self.GuiItems.items()

    def __len__(self) -> int:
        return len(self.GuiItems)

    @staticmethod
    def imgIn(imgPath: str) -> bool:
        region = pyautogui.locateOnScreen(imgPath, confidence=0.5, grayscale=True)
        return region is not None


class InGameAoE3GUIParser(GUIParser):
    icons_dir: str = os.getcwd() + r"\Icons"

    def setIcons(self):
        for filename in os.listdir(self.icons_dir):
            extension: str = ".PNG"
            if filename.endswith(extension):
                IconPath = os.path.join(self.icons_dir, filename)
                guiItem = GuiItem(name=filename.replace(extension, '')+"Icon",
                                  region=pyautogui.locateOnScreen(IconPath, confidence=0.8, grayscale=True),
                                  IconPath=IconPath)
                self.addItem(guiItem)

    def setResourceSlots(self):
        resources: dict = {
            "FoodIcon": "FoodSlot",
            "WoodIcon": "WoodSlot",
            "GoldIcon": "GoldSlot",
            "VillagersIcon": "HmVillagerSlot"
        }
        for resource, slotName in resources.items():
            resourceIconPos: tuple = self[resource].region
            slot = GuiItem(name=slotName, region=(resourceIconPos[0] + resourceIconPos[2], resourceIconPos[1],
                                                  resourceIconPos[2] * 1.9, resourceIconPos[3]),
                           char_whitelist="0123456789")
            self.addItem(slot)

    def setResourceCollectorsSlots(self):
        resources: dict = {
            "FoodIcon": "FoodCollectorsSlot",
            "WoodIcon": "WoodCollectorsSlot",
            "GoldIcon": "GoldCollectorsSlot",
            "VillagersIcon": "HmIdleVillagerSlot"
        }
        for resource, slotName in resources.items():
            resourceIconPos: tuple = self[resource].region
            slot = GuiItem(name=slotName, region=(resourceIconPos[0] - resourceIconPos[2], resourceIconPos[1],
                                                  resourceIconPos[2], resourceIconPos[3]),
                           char_whitelist="0123456789")
            self.addItem(slot)

    def setOptionsSlots(self):
        OptionsRegion = self["OptionsSlotsIcon"].box
        width, height = self["OptionSlotIcon"].box.width, self["OptionSlotIcon"].box.height
        for i in range(18):
            option = GuiItem(name=f"OptionSlot{i}", region=(OptionsRegion[0] + (i%6+2.7)*(OptionsRegion[2]/8.5),
                                                            OptionsRegion[1] + height*(i//6), width, height))
            self.addItem(option)

    def setMapItem(self):
        pass

    def setGuiItems(self):
        try:
            self.setIcons()
            self.setResourceSlots()
            self.setResourceCollectorsSlots()
            self.setOptionsSlots()
            self.setMapItem()
        except TypeError:
            print("--- setGuiItems --- Failed. Trying again in 5 s.")
            time.sleep(5)
            self.setGuiItems()


if __name__ == '__main__':
    import time

    time.sleep(1)
    InGameGui = InGameAoE3GUIParser()
    for _ in range(10):
        for name, item in InGameGui.items():
            item.show()

    InGameGui["FoodCollectorsSlot"].click()
