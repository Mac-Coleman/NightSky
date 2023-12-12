from PySide6.QtWidgets import QApplication, QDialog

from Satellite_Dialog.UI.SatelliteDialog import Ui_d_addSatellite

class SatelliteDialog(QDialog, Ui_d_addSatellite):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__data = None

    def accept(self):
        self.__data = self.le_name.text(), self.te_desc.toPlainText(), self.le_id.text()
        super().accept()

    def reject(self):
        self.__data = None
        super().reject()

    def data(self):
        return self.__data


if __name__ == "__main__":
    app = QApplication([])
    d = SatelliteDialog()
    d.exec()
    print(d.data())
