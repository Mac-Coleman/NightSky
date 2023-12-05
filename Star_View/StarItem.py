from PySide6.QtWidgets import QApplication, QGraphicsEllipseItem
from PySide6.QtGui import QPen, QBrush
from PySide6.QtCore import Qt

class StarItem(QGraphicsEllipseItem):

    pen = QPen(Qt.black, 1, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin)
    brush = QBrush(Qt.white)
    def __init__(self, pk, ra, dec, ap_mag, parent=None):
        super().__init__(parent)
        self.pk = pk
        self.ra = ra
        self.dec = dec
        self.size = (0.5 + 6 - ap_mag) ** 1.4

        self.setRect(ra, dec, self.size, self.size)
        self.setPen(StarItem.pen)
        self.setBrush(StarItem.brush)

    def updateCoords(self):
        t = QApplication.instance().skyTime
