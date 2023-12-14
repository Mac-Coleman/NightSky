import pandas
from PySide6.QtWidgets import QApplication, QGraphicsEllipseItem
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtCore import Qt

from Utils.utils import ra_dec_to_alt_az, zenith_angle_to_pole, azimuth_angle_to_pole, spherical_to_stereographic, polar_to_cartesian

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
        # self.updateCoords(0, 180)

    def updateCoords(self, poleAlt, poleAz):
        t = QApplication.instance().skyTime
        az, a, lst, h = ra_dec_to_alt_az(self.ra, self.dec, QApplication.instance().wgs84.latitude.degrees, QApplication.instance().wgs84.longitude.degrees, t)

        phi = zenith_angle_to_pole(poleAlt, poleAz, a, az)
        theta = azimuth_angle_to_pole(poleAlt, poleAz, a, az)

        r, theta = spherical_to_stereographic(phi, theta)
        y, x = polar_to_cartesian(r, theta)

        # self.setRect(-x*1000 - self.size/2, -y*1000 - self.size/2, self.size, self.size)
        return x, y

    def advance(self, phase: int) -> None:
        # super().advance(phase)
        x, y = self.updateCoords(self.scene().poleAltitude, self.scene().poleAzimuth)

        # print(self.pos(), end=' ')
        self.setRect(x * -1000, y * -1000, self.size, self.size)  # -x - self.size/2, -y - self.size/2)
        # print(self.pos())
