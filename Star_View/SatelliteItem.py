from PySide6.QtWidgets import QApplication, QGraphicsPixmapItem
from PySide6.QtGui import QPen, QBrush, QColor, QPixmap
from PySide6.QtCore import Qt

from Utils.utils import ra_dec_to_alt_az, zenith_angle_to_pole, azimuth_angle_to_pole, spherical_to_stereographic, polar_to_cartesian
import Icons_rc

class SatelliteItem(QGraphicsPixmapItem):

    pen = QPen(QColor.fromRgb(0, 0, 0, 0))
    brush = QBrush(Qt.white)
    def __init__(self, pk, sat, name, parent=None):
        super().__init__(parent)
        self.pk = pk
        self.sat = sat
        self.setToolTip(name)

        self.setPixmap(QPixmap(':/Icons/satellite-white').scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))

        self.altitude = 0
        self.azimuth = 0

    def updateAltAz(self):
        wgs84 = QApplication.instance().wgs84
        t = QApplication.instance().skyTime
        alt, az, _ = (self.sat - wgs84).at(t).altaz()
        self.altitude, self.azimuth = alt.degrees, az.degrees

    def updateCoords(self, poleAlt, poleAz):

        phi = zenith_angle_to_pole(poleAlt, poleAz, self.altitude, self.azimuth)
        theta = azimuth_angle_to_pole(poleAlt, poleAz, self.altitude, self.azimuth)

        r, theta = spherical_to_stereographic(phi, theta)
        y, x = polar_to_cartesian(r, theta)

        # self.setRect(-x*1000 - self.size/2, -y*1000 - self.size/2, self.size, self.size)
        return x, y

    def advance(self, phase: int) -> None:
        # super().advance(phase)
        x, y = self.updateCoords(self.scene().poleAltitude, self.scene().poleAzimuth)

        # print(self.pos(), end=' ')
        self.setPos(x * -self.scene().scale - 32, y * -self.scene().scale - 32)
        # self.setRect(x * -self.scene().scale, y * -self.scene().scale, 64, 64)  # -x - self.size/2, -y - self.size/2)
        # print(self.pos())
