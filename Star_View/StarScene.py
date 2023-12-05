from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsSceneMouseEvent
from PySide6.QtGui import QPen, QBrush
from PySide6.QtCore import Qt

from Star_View.StarItem import StarItem

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

        self._centerAltitude = 0.0
        self._centerAzimuth = 0.0

        stars = QApplication.instance().databaseManager.getBrightStars()

        pen = QPen(Qt.black, 1, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin)
        brush = QBrush(Qt.white)

        self.addEllipse(-1, -1, 2, 2, pen, brush)
        self.addEllipse(300, -1, 2, 2, pen, brush)

        for star in stars:
            star_item = StarItem(star[0], star[1], star[2], star[3])
            self.addItem(star_item)

        self._dragging = False

        QApplication.instance().updateTimer.timeout.connect(self.updateGraphicsItems)

    def updateGraphicsItems(self):
        print("graphics")

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

        self._centerAltitude += diff.y() * 0.1
        self._centerAzimuth -= diff.x() * 0.1

        self._centerAltitude = max(-89.0, min(89.0, self._centerAltitude))
        # self._centerAzimuth %= 360.0
        self._centerAzimuth = max(-360.0 * 2.5, min(self._centerAzimuth, 0))

        self.views()[0].centerOn(-self._centerAzimuth, self._centerAltitude)

        print(self._centerAltitude, self._centerAzimuth)
