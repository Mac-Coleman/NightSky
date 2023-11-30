from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from database import DatabaseManager

class NightSkyApp (QApplication):
    def __init__(self, args):
        super().__init__(args)

        self.databaseManager = DatabaseManager()

        self.satellites = []
        self.solarSystemObjects = []
        self.stars = []
        self.messierObjects = self.databaseManager.getMessierObjects()
        self.solarSystemObjects = self.databaseManager.getSolarSystemObjects()

