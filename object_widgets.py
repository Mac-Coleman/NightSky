# This Python file uses the following encoding: utf-8

import sys

from PySide6.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QFrame, QSizePolicy, QPushButton
from objects import SolarSystemObject, MessierObject
from database import TableSelection

class MessierObjectCard(QFrame):
    def __init__(self, object: MessierObject, parent=None):
        super().__init__(parent)
        self.object = object # Maintains a pointer to the Messier Object for which the card is based on

        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QGridLayout()

        title = QLabel("<b>" + self.object.alt_name + "</b>")

        ra_h, dec_d, dist_au = self.object.position.radec()

        ra = QLabel(str(ra_h))
        dec = QLabel(str(dec_d))

        favorite_button = QPushButton("Favorite")
        favorite_button.setCheckable(True)

        layout.addWidget(title, 0, 0, 1, 3)
        layout.addWidget(favorite_button, 0, 3, 1, 1)
        layout.addWidget(QLabel(self.object.type), 1, 0, 1, 4)

        layout.addWidget(QLabel("<b>RA:</b>"), 2, 0, 1, 1)
        layout.addWidget(ra, 2, 1, 1, 1)
        layout.addWidget(QLabel("<b>DE:</b>"), 3, 0, 1, 1)
        layout.addWidget(dec, 3, 1, 1, 1)

        layout.addWidget(QLabel("<b>AZ:</b>"), 2, 2, 1, 1)
        layout.addWidget(QLabel("123"), 2, 3, 1, 1)
        layout.addWidget(QLabel("<b>AL:</b>"), 3, 2, 1, 1)
        layout.addWidget(QLabel("123"), 3, 3, 1, 1)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.setLayout(layout)

class SolarSystemObjectCard(QFrame):
    def __init__(self, s: SolarSystemObject, parent=None):
        super().__init__(parent)
        self.object = s

        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QGridLayout()

        title = QLabel("<b>" + self.object.name + "</b>")

        ra = QLabel(str(0))
        dec = QLabel(str(0))

        favorite_button = QPushButton("Favorite")
        favorite_button.setCheckable(True)

        layout.addWidget(title, 0, 0, 1, 3)
        layout.addWidget(favorite_button, 0, 3, 1, 1)
        layout.addWidget(QLabel("EMPTY"), 1, 0, 1, 4)

        layout.addWidget(QLabel("<b>RA:</b>"), 2, 0, 1, 1)
        layout.addWidget(ra, 2, 1, 1, 1)
        layout.addWidget(QLabel("<b>DE:</b>"), 3, 0, 1, 1)
        layout.addWidget(dec, 3, 1, 1, 1)

        layout.addWidget(QLabel("<b>AZ:</b>"), 2, 2, 1, 1)
        layout.addWidget(QLabel("123"), 2, 3, 1, 1)
        layout.addWidget(QLabel("<b>AL:</b>"), 3, 2, 1, 1)
        layout.addWidget(QLabel("123"), 3, 3, 1, 1)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.setLayout(layout)

class ObjectCard(QWidget):
    def __init__(self, title: str, pk: int, favorited: bool, table: TableSelection, parent=None):
        self.pk = pk
        self.table = table

        super().__init__(parent)
        # self.setFrameShape(QFrame.Shape.HLine)
        layout = QGridLayout()
        t = QLabel(f"<b>{title}</b>")
        favorite_button = QPushButton("Favorite")
        favorite_button.setCheckable(True)
        favorite_button.setChecked(favorited)
        favorite_button.clicked.connect(self.handleFavorite)

        layout.addWidget(t, 0, 0, 1, 1)
        layout.addWidget(favorite_button, 0, 1, 1, 1)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setLayout(layout)
    
    def handleFavorite(self, checked):
        QApplication.instance().databaseManager.updateFavorite(self.pk, self.table, checked)

class ObjectSeparator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.HLine)





if __name__ == "__main__":

    o = MessierObject("M45", "Pleiades", "Open Cluster", 3.0, 192, 92, "Taurus", 40, 40, 3000)
    print(o)
    print([o])

    app = QApplication([])
    window = MessierObjectCard(o)
    window.show()
    sys.exit(app.exec())
