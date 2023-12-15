from PySide6.QtWidgets import QApplication, QWidget

from Settings_Menu.UI.SettingsMenu import Ui_w_settingsMenu

class SettingsMenu(QWidget, Ui_w_settingsMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pb_updateLocation.clicked.connect(self.handleLocationUpdate)

    def handleLocationUpdate(self):
        print("Updating")
        QApplication.instance().changeLocation(
            self.w_locationInput.location[0],
            self.w_locationInput.location[1],
            self.w_locationInput.location[2]
        )
        QApplication.instance().lookAt(0, 0)