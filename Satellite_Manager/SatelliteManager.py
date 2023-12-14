from PySide6.QtWidgets import QWidget, QHeaderView

from Satellite_Manager.UI.SatelliteManager import Ui_w_satelliteManager

from Satellite_Dialog.SatelliteDialog import SatelliteDialog


class SatelliteManager(QWidget, Ui_w_satelliteManager):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pb_add.clicked.connect(self.addSatellite)
        self.pb_clear.clicked.connect(self.clearSelected)
        self.pb_refreshAll.clicked.connect(self.refreshAll)
        self.pb_refreshOutOfDate.clicked.connect(self.refreshOutOfDate)
        self.pb_removeDecayed.clicked.connect(self.removeDecayed)
        self.pb_removeSelected.clicked.connect(self.removeSelected)

        self.tw_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        self.tw_table.itemSelectionChanged.connect(self.selectionChanged)

    def addSatellite(self):
        d = SatelliteDialog()
        d.exec()

    def clearSelected(self):
        self.tw_table.clearSelection()

    def refreshAll(self):
        pass

    def refreshOutOfDate(self):
        pass

    def removeDecayed(self):
        pass

    def removeSelected(self):
        pass

    def selectionChanged(self):
        if len(self.tw_table.selectedItems()) > 0:
            self.pb_clear.setEnabled(True)
            self.pb_removeSelected.setEnabled(True)
        else:
            self.pb_clear.setEnabled(False)
            self.pb_removeSelected.setEnabled(False)
            
if __name__ == "__main__":
    pass