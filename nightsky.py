from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, Signal

from skyfield.api import load, load_file, wgs84
from skyfield.toposlib import Topos

from database import DatabaseManager

class NightSkyApp (QApplication):

    lookAtInViewport = Signal(float, float)
    databaseUpdated = Signal()

    def __init__(self, args):
        super().__init__(args)

        self.databaseManager = DatabaseManager()

        self.satellites = []
        self.solarSystemObjects = []
        self.stars = []
        self.messierObjects = self.databaseManager.getMessierObjects()
        self.solarSystemObjects = self.databaseManager.getSolarSystemObjects()

        lat = 41.92
        lon = -91.42

        self.timescale = load.timescale()
        self.skyTime = self.timescale.now()
        self.ephemeris = load_file('de421.bsp')
        self.earth = self.ephemeris['Earth']
        self.geographic = self.earth + Topos(lat, lon)
        self.wgs84 = wgs84.latlon(lat, lon)

        self.updateTimer = QTimer()
        self.updateTimer.setInterval(5000) # Update every second
        self.updateTimer.timeout.connect(self.handleUpdateTimer)
        self.updateTimer.start()

    def handleUpdateTimer(self):
        self.skyTime = self.timescale.now()

    def changeLocation(self, lat, long, elevation):
        self.geographic = self.earth + Topos(lat, long, elevation_m=elevation)
        self.wgs84 = wgs84.latlon(lat, long, elevation_m=elevation)

    def lookAt(self, alt, az):
        self.lookAtInViewport.emit(alt, az)

    def cleanDatabaseData(self):
        self.databaseUpdated.emit()
