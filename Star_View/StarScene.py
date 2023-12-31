import math

from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsSceneWheelEvent, QGraphicsItemGroup
from PySide6.QtGui import QPen, QBrush, QTransform
from PySide6.QtCore import Qt

from skyfield.api import EarthSatellite

from Star_View.StarItem import StarItem
from Star_View.SatelliteItem import SatelliteItem
from Utils.utils import get_pole

class StarScene(QGraphicsScene):
    """
    The scene used by StarView.

    The point of this class is not to provide a picture-perfect representation of the night sky, but one that is
    good enough for hobbyist use in real time.

    Steps:
    RA/DEC -> local ALT/AZ -> stereographic projection with antipode of central ALT/AZ as pole.

    Cheats/Optimizations:
     - Display only those stars with magnitudes less than 6.0-6.5. (Somewhere between 4992 and 8785 stars)
     - Avoid using Skyfield operations on stars.
         - Largest parallax is less than one arcsecond, barely noticeable for most use cases.
         - Largest proper motion is only 10 arcseconds/year.
             - Largest proper motion of < 6.0 stars is 4.086 arcseconds/year...
             - about 2.1 arcminutes away from 1991.25 epoch
             - Probably don't need to consider it while drawing the stars.
     - Avoid using Skyfield operations on galaxies. It's not necessary at all really.
     - Use Skyfield operations for planets and satellites only.
     - Use simple functions for RA/DEC to ALT/AZ from: https://astrogreg.com/convert_ra_dec_to_alt_az.html
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(-1000, -1000, 2000, 2000)

        self._centerAltitude = 0.0
        self._centerAzimuth = 0.0

        self.poleAltitude, self.poleAzimuth = get_pole(self._centerAltitude, self._centerAzimuth)

        stars = QApplication.instance().databaseManager.getBrightStars()

        pen = QPen(Qt.black, 1, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin)
        brush = QBrush(Qt.GlobalColor.red)

        for star in stars:
            star_item = StarItem(star[0], star[1], star[2], star[3], star[4])
            star_item.updateAltAz()
            self.addItem(star_item)

        self.satellites = []

        self.setupSatellites()

        self.addEllipse(-5, -5, 10, 10, pen, brush)

        self.label = self.addSimpleText("Placeholder", "sans-serif")
        self.label.setBrush(QBrush(Qt.GlobalColor.white))

        # self.addItem(SatelliteItem(0, 0, "Test Satellite"))

        self._dragging = False
        self.scale = 1000

        self.advance()

        QApplication.instance().updateTimer.timeout.connect(self.updateItemCoordinates)
        QApplication.instance().lookAtInViewport.connect(self.lookAt)
        QApplication.instance().databaseUpdated.connect(self.setupSatellites)

    def advance(self) -> None:
        super().advance()
        self.label.setText(f"AltAz: {self._centerAltitude:.2f}, {self._centerAzimuth:.2f}")

        if len(self.views()) > 0:
            x = -self.views()[0].width()/2 + 10
            y = self.views()[0].height()/2 - 32
            self.label.setPos(x, y)

    def lookAt(self, alt, az):
        if math.isnan(alt) or math.isnan(az):
            return
        self._centerAzimuth = az
        self._centerAltitude = alt
        self.poleAltitude, self.poleAzimuth = get_pole(self._centerAltitude, self._centerAzimuth)
        self.advance()

    def setupSatellites(self):
        for sat in self.satellites:
            sat.setParentItem(None)
            del sat

        self.satellites = []

        satellites = QApplication.instance().databaseManager.getFavoriteSatellites()

        for sat in satellites:
            line0, line1, line2, *_ = sat[5].split("\n")
            es = EarthSatellite(line1, line2)
            sat_item = SatelliteItem(sat[0], es, sat[3])
            self.satellites.append(sat_item)
            self.addItem(sat_item)

    def updateItemCoordinates(self):

        for item in self.items():
            if type(item) is StarItem:
                item.updateAltAz()
                continue

            if type(item) is SatelliteItem:
                item.updateAltAz()
                continue

        self.advance()

    def setDragging(self, dragging):
        self._dragging = dragging
        if dragging:
            QApplication.instance().setOverrideCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            QApplication.instance().restoreOverrideCursor()

    def dragging(self):
        return self._dragging

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.setDragging(True)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.setDragging(False)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if not self._dragging:
            return
        diff = event.lastScreenPos() - event.screenPos()

        self._centerAltitude -= diff.y() * 0.1 # Dragging up should decrease altitude
        self._centerAzimuth += diff.x() * 0.1 # Dragging right should decrease azimuth

        self._centerAltitude = max(-89.0, min(89.0, self._centerAltitude))
        self._centerAzimuth %= 360.0
        # self._centerAzimuth = max(-360.0 * 2.5, min(self._centerAzimuth, 0))

        self.views()[0].centerOn(0, 0)

        self.poleAltitude, self.poleAzimuth = get_pole(self._centerAltitude, self._centerAzimuth)
        self.advance()

    def wheelEvent(self, event: QGraphicsSceneWheelEvent) -> None:
        event.accept()
        if event.delta() > 0 and self.scale < 7500:
            self.scale *= 1.1
        elif event.delta() < 0 and self.scale > 500:
            self.scale /= 1.1
        self.advance()