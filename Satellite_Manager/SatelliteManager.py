import datetime

from PySide6.QtWidgets import QApplication, QWidget, QHeaderView, QTableWidget, QTableWidgetItem

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

        self.pb_clear.setEnabled(False)
        self.pb_removeSelected.setEnabled(False)

        self.tw_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        self.tw_table.itemSelectionChanged.connect(self.selectionChanged)
        self.tw_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.primary_keys = []
        self.reloadRows()



    def reloadRows(self):

        self.tw_table.setRowCount(0)
        self.primary_keys = []

        satellites = QApplication.instance().databaseManager.getAllSatellites()

        for sat in satellites:
            self.primary_keys.append(sat[0])
            self.tw_table.insertRow(self.tw_table.rowCount())
            self.tw_table.setItem(self.tw_table.rowCount() - 1,
                                  0,
                                  QTableWidgetItem(sat[3]))

            self.tw_table.setItem(self.tw_table.rowCount() - 1,
                                  1,
                                  QTableWidgetItem(datetime.datetime.fromtimestamp(sat[6]).strftime("%Y-%m-%d")))

            self.tw_table.setItem(self.tw_table.rowCount() - 1,
                                  2,
                                  QTableWidgetItem(sat[2]))

    def addSatellite(self):
        d = SatelliteDialog()
        d.exec()

        if d.data() is not None:
            try:
                name, desc, id = d.data()
                QApplication.instance().databaseManager.addSatellite(name, desc, id)
                self.reloadRows()
            except ValueError:
                print("Nope!")

    def clearSelected(self):
        self.tw_table.clearSelection()

    def refreshAll(self):
        try:
            QApplication.instance().databaseManager.refreshAll()
        except ValueError:
            print("Failed to update.")
        self.reloadRows()

    def refreshOutOfDate(self):
        try:
            QApplication.instance().databaseManager.refreshOutOfDate()
        except ValueError:
            print("Failed to update.")
        self.reloadRows()

    def removeDecayed(self):
        QApplication.instance().databaseManager.deleteDecayed()
        self.reloadRows()

    def removeSelected(self):
        model = self.tw_table.selectionModel()
        selection = model.selectedRows()

        for row in selection:
            pk = self.primary_keys[row.row()]
            QApplication.instance().databaseManager.deleteSatellite(pk)

        self.reloadRows()

    def selectionChanged(self):
        if len(self.tw_table.selectedItems()) > 0:
            self.pb_clear.setEnabled(True)
            self.pb_removeSelected.setEnabled(True)
        else:
            self.pb_clear.setEnabled(False)
            self.pb_removeSelected.setEnabled(False)
            
if __name__ == "__main__":
    pass