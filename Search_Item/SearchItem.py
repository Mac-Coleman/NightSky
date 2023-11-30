import sys
import webbrowser

import skyfield.api
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer

from skyfield.api import load, load_file, wgs84, Topos
from skyfield.magnitudelib import planetary_magnitude
from skyfield.starlib import Star
from skyfield.sgp4lib import EarthSatellite

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

    def updateDist(self, dist, unit):
        s = f"<b>{dist:0.2f} {unit}</b>"
        self.lb_distance.setText(s)

    def updateMag(self, mag):
        s = f"<b>{mag:0.2f}</b>"
        self.lb_magnitude.setText(s)

    def updateAlt(self, alt):
        s = f"<b>{alt}</b>"
        self.lb_altitude.setText(s.replace("deg", "°"))

    def updateAz(self, az):
        s = f"<b>{az}</b>"
        self.lb_azimuth.setText(s.replace("deg", "°"))

class SatelliteItem(SearchItem):
    def __init__(self, title, desc, skyfield_object, norad_id):
        super().__init__(title, desc, skyfield_object)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/satellite-communication.svg"))
        self.lb_magnitude.setText("<b>Unknown</b>")
        self.norad_id = norad_id
        self.pb_infoButton.clicked.connect(self.handleInfo)

    def updatePosition(self):
        skyTime = QApplication.instance().skyTime
        wgs84Position = QApplication.instance().wgs84

        difference = self.object - wgs84Position
        topocentric = difference.at(skyTime)

        radec = topocentric.radec()
        altaz = topocentric.altaz()

        self.updateRA(radec[0])
        self.updateDEC(radec[1])
        self.updateDist(radec[2].km, "km")

        self.updateAlt(altaz[0])
        self.updateAz(altaz[1])

    def handleInfo(self):
        webbrowser.open(f"https://www.n2yo.com/?s={self.norad_id}")

class PlanetItem(SearchItem):
    def __init__(self, title, desc, skyfield_object):
        super().__init__(title, desc, skyfield_object)
        self.title = title
        self.lb_icon.setPixmap(QPixmap(u":/Icons/solar-system.svg"))

        self.pb_infoButton.clicked.connect(self.handleInfo)

    def updatePosition(self):
        skyTime = QApplication.instance().skyTime
        geographic = QApplication.instance().geographic

        astrometric = geographic.at(skyTime).observe(self.object).apparent()
        radec = astrometric.radec()
        altaz = astrometric.altaz()

        self.updateRA(radec[0])
        self.updateDEC(radec[1])
        self.updateDist(radec[2].au, "au")

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
    def __init__(self, title, desc, skyfield_object, apparent_magnitude, hip):
        super().__init__(title, desc, skyfield_object)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/polar-star.svg"))
        self.lb_magnitude.setText(f"<b>{apparent_magnitude:0.2f}</b>")
        self.hip = hip
        self.pb_infoButton.clicked.connect(self.handleInfo)

    def updatePosition(self):
        skyTime = QApplication.instance().skyTime
        geographic = QApplication.instance().geographic

        astrometric = geographic.at(skyTime).observe(self.object).apparent()
        radec = astrometric.radec()
        altaz = astrometric.altaz()

        self.updateRA(radec[0])
        self.updateDEC(radec[1])
        self.updateDist(radec[2].au * 1.58125e-5, "ly")

        self.updateAlt(altaz[0])
        self.updateAz(altaz[1])

    def handleInfo(self):
        webbrowser.open(f"https://simbad.u-strasbg.fr/simbad/sim-basic?Ident=HIP{self.hip}&submit=SIMBAD+search")

class MessierItem(SearchItem):
    def __init__(self, title, desc, skyfield_object, apparent_magnitude, distance, messier):
        super().__init__(title, desc, skyfield_object)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/galaxy.svg"))
        self.lb_magnitude.setText(f"<b>{apparent_magnitude:0.2f}</b>")
        self.updateDist(distance, 'ly')

        self.messier = messier.replace("M", "Messier_")
        self.pb_infoButton.clicked.connect(self.handleInfo)

    def updatePosition(self):
        skyTime = QApplication.instance().skyTime
        geographic = QApplication.instance().geographic

        astrometric = geographic.at(skyTime).observe(self.object).apparent()
        radec = astrometric.radec()
        altaz = astrometric.altaz()

        self.updateRA(radec[0])
        self.updateDEC(radec[1])

        self.updateAlt(altaz[0])
        self.updateAz(altaz[1])

    def handleInfo(self):
        webbrowser.open(f"https://en.wikipedia.org/wiki/{self.messier}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ephemeris = load_file("../de421.bsp")

    lat = 41.92
    lon = -91.42

    ts = load.timescale()
    app.earth = ephemeris["Earth"]
    app.skyTime = ts.now()
    app.geographic = app.earth + Topos(lat, lon)
    app.wgs84 = wgs84.latlon(lat, lon)

    planet = ephemeris["Mercury"]

    # s = PlanetItem("Mercury", "The second planet from the sun", planet)
    barnard = Star(ra_hours=(17, 57, 48.49803),
                   dec_degrees=(4, 41, 36.2072),
                   ra_mas_per_year=-798.71,
                   dec_mas_per_year=10337.77,
                   parallax_mas=545.4,
                   radial_km_per_s=-110.6)
    # s = StarItem("Barnard's Star", "The star moving fastest across our sky.", barnard, 9.51, "87937")
    pleiades = Star(ra_hours=(8, 40, 6),
                    dec_degrees=(24, 7, 12))
    # s = MessierItem("The Pleiades", "Messier 45, an open cluster of many blue stars.", pleiades, 1.6, 444, "M45")

    # This TLE might be outdated by the time you're testing this... I'm just using this one for testing.
    # Last Retrieved from Celestrak on 11/29/2023
    line1 = "1 25544U 98067A   23333.91619101  .00024169  00000+0  43094-3 0  9996"
    line2 = "2 25544  51.6417 227.6788 0001060 344.9414 118.7978 15.49949661427493"
    iss = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)

    s = SatelliteItem('The ISS', "The International Space Station, the largest crewed spacecraft.", iss, "25544")

    def handleTimer():
        app.skyTime = ts.now()
        s.updatePosition()

    timer = QTimer()
    timer.setInterval(500)
    timer.timeout.connect(handleTimer)
    timer.start()

    s.show()
    s.updatePosition()

    print(app.geographic)

    sys.exit(app.exec())