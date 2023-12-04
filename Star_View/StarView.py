import sys

from Star_View.StarScene import StarScene

from PySide6.QtWidgets import QApplication, QGraphicsView
from PySide6.QtCore import Qt


class StarView(QGraphicsView):
    """
    Displays a graphical representation of the night sky.
    Camera position and orientation is based on the observer's local azimuth/altitude.
    Uses StarScene to draw the actual stars.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = StarScene(self)
        self.setScene(self.scene)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)




if __name__ == "__main__":
    app = QApplication()
    view = StarView()
    view.show()
    sys.exit(app.exec())