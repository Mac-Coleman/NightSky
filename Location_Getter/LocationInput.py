import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap

from Location_Getter.UI.LocationInput import Ui_w_LocationInput

class LocationInput(QWidget, Ui_w_LocationInput):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    i = LocationInput()
    i.show()

    sys.exit(app.exec())