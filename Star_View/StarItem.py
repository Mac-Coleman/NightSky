import pandas
from PySide6.QtWidgets import QApplication, QGraphicsEllipseItem
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtCore import Qt

from Utils.utils import ra_dec_to_alt_az

class StarItem(QGraphicsEllipseItem):

    pen = QPen(QColor.fromRgb(0, 0, 0, 0))
    brush = QBrush(Qt.white)
    def __init__(self, pk, ra, dec, ap_mag, parent=None):
        super().__init__(parent)
        self.pk = pk
        self.ra = ra
        self.dec = dec
        self.size = (1 + 6 - ap_mag) ** 1.4
        #self.setPen(StarItem.pen)
        self.setBrush(StarItem.brush)

        self.setRect(ra*10 - self.size/2, dec*10 - self.size/2, self.size, self.size)
        self.updateCoords()

    def updateCoords(self):
        t = pandas.Timestamp(year=1999, month=12, day=1, hour=10, minute=16, second=0)
        print(t.tzname())
        t = t.to_julian_date()
        t = QApplication.instance().skyTime
        az, a, lst, h = ra_dec_to_alt_az(self.ra, self.dec, QApplication.instance().wgs84.latitude.degrees, QApplication.instance().wgs84.longitude.degrees, t)

        self.setRect(az*2.5 - self.size/2, a*2.5 - self.size/2, self.size, self.size)
