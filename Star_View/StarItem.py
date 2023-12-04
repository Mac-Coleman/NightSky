from PySide6.QtWidgets import QApplication, QGraphicsItem

class StarItem(QGraphicsItem):
    def __init__(self, pk, ra, dec, parent=None):
        super().__init__(parent)
        self.pk = pk
        self.ra = ra
        self.dec = dec

    def updateCoords(self):
        t = QApplication.instance().skyTime
