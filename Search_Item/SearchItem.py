import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap

from Search_Item.UI.SearchItem import Ui_w_SearchItem


class SearchItem(QWidget, Ui_w_SearchItem):
    def __init__(self, title, desc):
        super().__init__()
        self.setupUi(self)
        self.lb_title.setText(f"<h1>{title}</h1>")
        self.lb_description.setText(desc)


class SatelliteItem(SearchItem):
    def __init__(self, title, desc):
        super().__init__(title, desc)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/satellite-communication.svg"))


class PlanetItem(SearchItem):
    def __init__(self, title, desc):
        super().__init__(title, desc)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/solar-system.svg"))

class StarItem(SearchItem):
    def __init__(self, title, desc):
        super().__init__(title, desc)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/polar-star.svg"))

class MessierItem(SearchItem):
    def __init__(self, title, desc):
        super().__init__(title, desc)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/galaxy.svg"))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    s = MessierItem("The Moon", "The moon is the earth's natural satellite.")
    s.show()

    sys.exit(app.exec())