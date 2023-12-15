import sys
from PySide6.QtWidgets import QApplication, QWidget
import geocoder

from Location_Getter.UI.LocationInput import Ui_w_LocationInput

class LocationInput(QWidget, Ui_w_LocationInput):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.updateLocationRaw()

        self.db_latitude.valueChanged.connect(self.updateLocationRaw)
        self.db_longitude.valueChanged.connect(self.updateLocationRaw)
        self.db_elevation.valueChanged.connect(self.updateElevationRaw)

        self.pb_automatic.clicked.connect(self.geocoder)

        self.location = (0.0, 0.0, 0.0)

    def updateLocationRaw(self):
        self.location = (
            float(self.db_latitude.value()),
            float(self.db_longitude.value()),
            float(self.db_elevation.value())
        )

        la = "N" if self.location[0] > 0 else "S"
        lo = "E" if self.location[1] > 0 else "W"

        self.lb_selection.setText(f"Selected Location: {abs(self.location[0])}°{la}, {abs(self.location[1])}°{lo}, {self.location[2]} m")
        self.lb_human.setText("Near <i>unknown</i>")

    def updateElevationRaw(self):
        self.location = (
            float(self.db_latitude.value()),
            float(self.db_longitude.value()),
            float(self.db_elevation.value())
        )

        la = "N" if self.location[0] > 0 else "S"
        lo = "E" if self.location[1] > 0 else "W"

        self.lb_selection.setText(
            f"Selected Location: {abs(self.location[0])}°{la}, {abs(self.location[1])}°{lo}, {self.location[2]} m")

    def geocoder(self):
        g = geocoder.ip('me')
        self.db_latitude.setValue(g.latlng[0])
        self.db_longitude.setValue(g.latlng[1])

        self.lb_human.setText(f"Near <i>{g.city}, {g.country}</i>")



if __name__ == "__main__":
    app = QApplication(sys.argv)

    i = LocationInput(None)
    i.show()

    sys.exit(app.exec())