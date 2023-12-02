# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QHBoxLayout, QVBoxLayout, QTabWidget, QPushButton, QWidget, QLineEdit, QScrollArea, QLabel, QFrame, QSizePolicy, QSplitter
from PySide6.QtGui import QFont, QIcon
import random

from database import DatabaseManager
from object_widgets import MessierObjectCard, ObjectSeparator
from nightsky import NightSkyApp

from Hello_Dialog.HelloDialog import HelloDialog


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Night Skies")
        self.setMinimumSize(1000, 500)


        splitter = QSplitter()
        graphics = QGraphicsView()
        scene = QGraphicsScene(-1.0, -1.0, 2.0, 2.0)
        l = scene.addText("Stars go here", QFont("SansSerif", pointSize=25))
        l.setPos(-100, -25)

        for i in range(1, 256):
            a = scene.addText(random.choice("*-.'`"))
            a.setPos((random.random()-0.5) * 625, (random.random()-0.5) * 500)

        graphics.setScene(scene)

        splitter.addWidget(graphics)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)

        tabs.addTab(NotificationTab(), "Notifications")
        tabs.addTab(NotificationTab(), "All Events")
        tabs.addTab(ObjectTab(), "Objects")
        tabs.addTab(QPushButton("What on earth"), "Settings")

        splitter.addWidget(tabs)

        self.setCentralWidget(splitter)

class NotificationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        contentsArea = QScrollArea()

        contentLayout = QVBoxLayout()

        contentLayout.addWidget(NotificationCard(title="Solar Eclipse", desc="The moon will eclipse the sun."))
        contentLayout.addWidget(NotificationCard(title="ISS Pass", desc="The international space station will pass overhead tonight, 8:31PM, WNW-SE, 78 degrees altitude"))
        contentLayout.addWidget(NotificationCard(title="Tiangong Pass", desc="Tiangong will pass overhead tomorrow night, 7:49 PM, SSW-E, 81 degrees altitude"))
        contentLayout.addWidget(NotificationCard(title="Heliacal Rising of the Pleiades", desc="The Pleiades open star cluster will rise again in the Eastern Sky."))
        contentLayout.addWidget(NotificationCard(title="Lunar Eclipse", desc="The earth will eclipse the moon."))
        contentLayout.addWidget(NotificationCard(title="ISS Transit of the moon", desc="The international space station will transit the moon."))
        contentLayout.addWidget(NotificationCard(title="ISS Transit of the moon", desc="The international space station will transit the moon."))
        contentLayout.addWidget(NotificationCard(title="ISS Transit of the moon", desc="The international space station will transit the moon."))



        contents = QWidget()
        contents.setLayout(contentLayout)


        contentsArea.setWidget(contents)

        layout.addWidget(SearchBar())
        layout.addWidget(TypeFilter())
        layout.addWidget(contentsArea)

        self.setLayout(layout)

class NotificationCard(QFrame):
    def __init__(self, parent=None, title="", desc=""):
        super().__init__(parent)

        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout()
        titleLabel = QLabel(f"<b>{title}</b>")
        titleLabel.setWordWrap(True)
        titleLabel.setTextFormat(Qt.TextFormat.RichText)

        descLabel = QLabel(desc)
        descLabel.setWordWrap(True)

        layout.addWidget(titleLabel)
        layout.addWidget(descLabel)
        self.setLayout(layout)

class ObjectTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.addTab(ObjectList(True, False), "Tracked")
        tabs.addTab(ObjectList(False, True), "All")

        layout.addWidget(tabs)

        self.setLayout(layout)

class ObjectList(QWidget):
    def __init__(self, favoritesOnly: bool, defaultEmpty: bool, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        contents = QScrollArea()
        contents.setLayout(QHBoxLayout())

        self.objectFilterer = ObjectFilterer()

        layout.addWidget(self.objectFilterer)
        layout.addWidget(contents)

        self.contentLayout = QVBoxLayout()

        contentsWidget = QWidget()
        # Make sure that it gets enough space for itself and all its contents
        contentsWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        contentsWidget.setLayout(self.contentLayout)
        contents.setWidget(contentsWidget)

        self.setLayout(layout)

        # Now to connect the slots and signals for the object filterer
        self.objectFilterer.searchBar.bar.editingFinished.connect(self.handleEditingFinished)
        self.objectFilterer.typeFilter.satelliteButton.clicked.connect(self.handleSatelliteButton)
        self.objectFilterer.typeFilter.solarSystemButton.clicked.connect(self.handlePlanetButton)
        self.objectFilterer.typeFilter.starButton.clicked.connect(self.handleStarsButton)
        self.objectFilterer.typeFilter.messierButton.clicked.connect(self.handleMessierButton)

        # Prepare search results
        self.searchResults = []

        # Prepare search type filters
        self.satellitesHidden = False
        self.solarSystemHidden = False
        self.starsHidden = False
        self.messierHidden = False

        self.favoritesOnly = favoritesOnly
        self.defaultEmpty = defaultEmpty

        self.handleEditingFinished()

    def handleEditingFinished(self):
        print("Finished typing")
        query = self.objectFilterer.searchBar.bar.text()

        for i in reversed(range(self.contentLayout.count())):
            self.contentLayout.itemAt(i).widget().setParent(None)

        if self.defaultEmpty and query == "":
            return
        
        widgets = []
        
        if not self.satellitesHidden:
            QApplication.instance().databaseManager.searchSatellites(query, self.favoritesOnly)

        if not self.solarSystemHidden:
            widgets += QApplication.instance().databaseManager.searchSolarSystem(query, self.favoritesOnly)

        if not self.starsHidden:
            widgets += QApplication.instance().databaseManager.searchStars(query, self.favoritesOnly)

        if not self.messierHidden:
            widgets += QApplication.instance().databaseManager.searchMessier(query, self.favoritesOnly)

        for result in widgets:
            self.contentLayout.addWidget(result)
            result.setVisible(True)
            sep = ObjectSeparator()
            sep.setVisible(True)
            self.contentLayout.addWidget(sep)
            self.contentLayout.parentWidget().adjustSize()



    def handleSatelliteButton(self, checked):
        self.satellitesHidden = checked
        self.handleEditingFinished()

    def handlePlanetButton(self, checked):
        self.solarSystemHidden = checked
        self.handleEditingFinished()

    def handleStarsButton(self, checked):
        self.starsHidden = checked
        self.handleEditingFinished()

    def handleMessierButton(self, checked):
        self.messierHidden = checked
        self.handleEditingFinished()

class ObjectFilterer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.searchBar = SearchBar()
        self.typeFilter = TypeFilter()

        layout.addWidget(self.searchBar)
        layout.addWidget(self.typeFilter)

        self.setLayout(layout)

import Icons_rc

class SearchBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()

        self.bar = QLineEdit()
        self.bar.setPlaceholderText("Filter...")
        self.bar.setClearButtonEnabled(True)

        button = QPushButton()
        button.setIcon(QIcon(":/Icons/magnifying-glass-white"))

        layout.addWidget(self.bar)
        layout.addWidget(button)
        self.setLayout(layout)

class TypeFilter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()

        self.satelliteButton = QPushButton("Satellites")
        self.satelliteButton.setCheckable(True)

        self.solarSystemButton = QPushButton("Planets")
        self.solarSystemButton.setCheckable(True)

        self.starButton = QPushButton("Stars")
        self.starButton.setCheckable(True)

        self.messierButton = QPushButton("Deep Sky")
        self.messierButton.setCheckable(True)

        self.satelliteButton.setIcon(QIcon(":/Icons/satellite-white"))
        self.solarSystemButton.setIcon(QIcon(":/Icons/solar-system-white"))
        self.starButton.setIcon(QIcon(":/Icons/star-white"))
        self.messierButton.setIcon(QIcon(":/Icons/galaxy-white"))

        layout.addWidget(self.satelliteButton)
        layout.addWidget(self.solarSystemButton)
        layout.addWidget(self.starButton)
        layout.addWidget(self.messierButton)
        self.setLayout(layout)


if __name__ == "__main__":

    app = NightSkyApp([])
    main_window = MainWindow()
    main_window.show()
    startup_dialog = HelloDialog()

    def handleStartup(status):
        if status:
            lat, long, elev = startup_dialog.getLocation()
            app.changeLocation(lat, long, elev)


    startup_dialog.finished.connect(handleStartup)
    startup_dialog.open()
    sys.exit(app.exec())
