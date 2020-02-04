import cv2


class Unit:
    def __init__(self, name: str, IconPath: str):
        self.name = name
        self.IconPath = IconPath

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


if __name__ == '__main__':
    pass
