import sys
import webbrowser

import skyfield.api
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap

from skyfield.api import load, load_file, Topos
from skyfield.magnitudelib import planetary_magnitude

from Search_Item.UI.SearchItem import Ui_w_SearchItem


class SearchItem(QWidget, Ui_w_SearchItem):
    def __init__(self, title, desc, skyfield_object):
        super().__init__()
        self.setupUi(self)
        self.lb_title.setText(f"<h1>{title}</h1>")
        self.lb_description.setText(desc)

        self.object = skyfield_object

    def updatePosition(self):
        pass

    def updateRA(self, angle):
        s = f"<b>{angle}</b>"
        self.lb_rightAscension.setText(s)

    def updateDEC(self, angle):
        s = f"<b>{angle.dstr()}</b>"
        self.lb_declination.setText(s.replace("deg", "°"))

    def updateDist(self, dist):
        s = f"<b>{dist}</b>"
        self.lb_distance.setText(s)

    def updateMag(self, mag):
        s = f"<b>{mag}</b>"
        self.lb_magnitude.setText(s)

    def updateAlt(self, alt):
        s = f"<b>{alt}</b>"
        self.lb_altitude.setText(s.replace("deg", "°"))

    def updateAz(self, az):
        s = f"<b>{az}</b>"
        self.lb_azimuth.setText(s.replace("deg", "°"))

class SatelliteItem(SearchItem):
    def __init__(self, title, desc, skyfield_object):
        super().__init__(title, desc, skyfield_object)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/satellite-communication.svg"))


class PlanetItem(SearchItem):
    def __init__(self, title, desc, skyfield_object):
        super().__init__(title, desc, skyfield_object)
        self.title = title
        self.lb_icon.setPixmap(QPixmap(u":/Icons/solar-system.svg"))

        self.pb_infoButton.clicked.connect(self.handleInfo)

    def updatePosition(self):
        earth = QApplication.instance().earth
        skyTime = QApplication.instance().skyTime
        geographic = QApplication.instance().geographic

        astrometric = geographic.at(skyTime).observe(self.object).apparent()
        radec = astrometric.radec()
        altaz = astrometric.altaz()
        print(altaz)

        self.updateRA(radec[0])
        self.updateDEC(radec[1])
        self.updateDist(radec[2])

        self.updateAlt(altaz[0])
        self.updateAz(altaz[1])

        try:
            self.updateMag(planetary_magnitude(astrometric))
        except ValueError:
            self.updateMag("Unknown")

    def handleInfo(self):
        if self.title == "Mercury":
            self.title = "Mercury (planet)"
        webbrowser.open("https://en.wikipedia.org/wiki/" + self.title.replace(" ", "_"))


class StarItem(SearchItem):
    def __init__(self, title, desc, skyfield_object):
        super().__init__(title, desc, skyfield_object)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/polar-star.svg"))

    def updatePosition(self):
        earth = QApplication.instance().earth
        skyTime = QApplication.instance().skyTime

        astrometric = earth.at(skyTime).apparent(self.object)
        print(astrometric.radec())

class MessierItem(SearchItem):
    def __init__(self, title, desc, skyfield_object):
        super().__init__(title, desc, skyfield_object)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/galaxy.svg"))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ephemeris = load_file("../de421.bsp")
    planet = ephemeris["Mercury"]

    app.earth = ephemeris["Earth"]
    app.skyTime = load.timescale().now()
    app.geographic = app.earth + Topos(41.92, -91.42)

    s = PlanetItem("Mercury", "The second planet from the sun", planet)
    s.show()
    s.updatePosition()

    print(app.geographic)

    sys.exit(app.exec())