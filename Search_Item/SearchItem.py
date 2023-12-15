import sys
import webbrowser

import skyfield.api
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, Slot

from skyfield.api import load, load_file, wgs84, Topos
from skyfield.magnitudelib import planetary_magnitude
from skyfield.starlib import Star
from skyfield.sgp4lib import EarthSatellite
from skyfield.units import Angle

from Search_Item.UI.SearchItem import Ui_w_SearchItem

from database import TableSelection


class SearchItem(QWidget, Ui_w_SearchItem):
    def __init__(self, pk, favorited, title, desc, skyfield_object):
        super().__init__()
        self.setupUi(self)
        self.lb_title.setText(f"<h1>{title}</h1>")
        self.lb_description.setText(desc)

        self.object = skyfield_object
        self.pk = pk
        self.pb_likeButton.setChecked(favorited)
        self.pb_likeButton.clicked.connect(self.handleFavorite)
        self.pb_observeButton.clicked.connect(self.handleObserve)

        self.altitude = 0
        self.azimuth = 0



    @Slot()
    def updatePosition(self):
        print("received")
        pass

    def updateRA(self, angle):
        s = f"<b>{angle}</b>"
        self.lb_rightAscension.setText(s)

    def updateDEC(self, angle):
        s = angle
        if type(angle) is Angle:
            s = f"<b>{angle.dstr()}</b>"
        self.lb_declination.setText(s.replace("deg", "°"))

    def updateDist(self, dist, unit):
        s = f"<b>{dist:0.2f} {unit}</b>"
        self.lb_distance.setText(s)

    def updateMag(self, mag):
        s = f"<b>{mag:0.2f}</b>" if type(mag) == float else f"<b>{mag}</b>"
        self.lb_magnitude.setText(s)

    def updateAlt(self, alt):
        s = f"<b>{alt}</b>"
        self.lb_altitude.setText(s.replace("deg", "°"))

    def updateAz(self, az):
        s = f"<b>{az}</b>"
        self.lb_azimuth.setText(s.replace("deg", "°"))

    def handleFavorite(self, checked):
        pass

    def handleObserve(self):
        QApplication.instance().lookAt(self.altitude, self.azimuth)

class SatelliteItem(SearchItem):
    def __init__(self, pk, favorited, title, desc, skyfield_object, norad_id):
        super().__init__(pk, favorited, title, desc, skyfield_object)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/satellite-white"))
        self.lb_magnitude.setText("<b>Unknown</b>")
        self.norad_id = norad_id
        self.pb_infoButton.clicked.connect(self.handleInfo)

        try:
            QApplication.instance().updateTimer.timeout.connect(self.updatePosition)
        except AttributeError as e:
            print(e)
            print("Running in test mode?")

    def updatePosition(self):
        if self.visibleRegion().isEmpty():
            return
        radec = ["unknown", "unknown", 0.00]
        altaz = ["unknown", "unknown"]

        if self.object is not None:
            skyTime = QApplication.instance().skyTime
            wgs84Position = QApplication.instance().wgs84

            difference = self.object - wgs84Position
            topocentric = difference.at(skyTime)

            radec = topocentric.radec()
            altaz = topocentric.altaz()
            self.altitude, self.azimuth = altaz[0].degrees, altaz[1].degrees

        self.updateRA(radec[0])
        self.updateDEC(radec[1])

        if type(radec[2]) is float:
            self.updateDist(radec[2], "")
        else:
            self.updateDist(radec[2].km, "km")

        self.updateAlt(altaz[0])
        self.updateAz(altaz[1])

    def handleInfo(self):
        webbrowser.open(f"https://www.n2yo.com/?s={self.norad_id}")

    def handleFavorite(self, checked):
        QApplication.instance().databaseManager.updateFavorite(self.pk, TableSelection.SATELLITE, checked)

class PlanetItem(SearchItem):
    def __init__(self, pk, favorited, title, desc, skyfield_object):
        super().__init__(pk, favorited, title, desc, skyfield_object)
        self.title = title
        self.lb_icon.setPixmap(QPixmap(u":/Icons/solar-system-white"))

        self.pb_infoButton.clicked.connect(self.handleInfo)

        try:
            QApplication.instance().updateTimer.timeout.connect(self.updatePosition)
        except AttributeError as e:
            print(e)
            print("Running in test mode?")

    def updatePosition(self):
        if self.visibleRegion().isEmpty():
            return

        skyTime = QApplication.instance().skyTime
        geographic = QApplication.instance().geographic

        astrometric = geographic.at(skyTime).observe(self.object).apparent()
        radec = astrometric.radec()
        altaz = astrometric.altaz()

        self.altitude, self.azimuth = altaz[0].degrees, altaz[1].degrees

        self.updateRA(radec[0])
        self.updateDEC(radec[1])
        self.updateDist(radec[2].au, "au")

        self.updateAlt(altaz[0])
        self.updateAz(altaz[1])

        try:
            self.updateMag(float(planetary_magnitude(astrometric)))
        except ValueError:
            self.updateMag("Unknown")

    def handleInfo(self):
        if self.title == "Mercury":
            self.title = "Mercury (planet)"
        if self.title == "The Sun (Sol)":
            self.title = "Sun"
        webbrowser.open("https://en.wikipedia.org/wiki/" + self.title.replace(" ", "_"))

    def handleFavorite(self, checked):
        QApplication.instance().databaseManager.updateFavorite(self.pk, TableSelection.SOLAR_SYSTEM, checked)


class StarItem(SearchItem):
    def __init__(self, pk, favorited, title, desc, skyfield_object, apparent_magnitude, hip):
        super().__init__(pk, favorited, title, desc, skyfield_object)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/star-white"))
        self.lb_magnitude.setText(f"<b>{apparent_magnitude:0.2f}</b>")
        self.hip = hip
        self.pb_infoButton.clicked.connect(self.handleInfo)

        try:
            QApplication.instance().updateTimer.timeout.connect(self.updatePosition)
        except AttributeError as e:
            print(e)
            print("Running in test mode?")

    def updatePosition(self):
        if self.visibleRegion().isEmpty():
            return

        skyTime = QApplication.instance().skyTime
        earth = QApplication.instance().earth
        topocentric = QApplication.instance().wgs84

        apparent = (earth + topocentric).at(skyTime).observe(self.object).apparent()
        radec = apparent.radec()
        altaz = apparent.altaz()

        self.altitude, self.azimuth = altaz[0].degrees, altaz[1].degrees

        self.updateRA(radec[0])
        self.updateDEC(radec[1])
        self.updateDist(radec[2].au * 1.58125e-5, "ly")

        self.updateAlt(altaz[0])
        self.updateAz(altaz[1])

    def handleInfo(self):
        webbrowser.open(f"https://simbad.u-strasbg.fr/simbad/sim-basic?Ident=HIP{self.hip}&submit=SIMBAD+search")

    def handleFavorite(self, checked):
        QApplication.instance().databaseManager.updateFavorite(self.pk, TableSelection.STAR, checked)

class MessierItem(SearchItem):
    def __init__(self, pk, favorited, title, desc, skyfield_object, apparent_magnitude, distance, messier):
        super().__init__(pk, favorited, title, desc, skyfield_object)
        self.lb_icon.setPixmap(QPixmap(u":/Icons/galaxy-white"))
        self.lb_magnitude.setText(f"<b>{apparent_magnitude:0.2f}</b>")
        self.updateDist(distance, 'ly')

        self.messier = messier.replace("M", "Messier_")
        self.pb_infoButton.clicked.connect(self.handleInfo)

        try:
            QApplication.instance().updateTimer.timeout.connect(self.updatePosition)
        except AttributeError as e:
            print(e)
            print("Running in test mode?")

    def updatePosition(self):
        if self.visibleRegion().isEmpty():
            return

        skyTime = QApplication.instance().skyTime
        geographic = QApplication.instance().geographic

        astrometric = geographic.at(skyTime).observe(self.object).apparent()
        radec = astrometric.radec()
        altaz = astrometric.altaz()

        self.altitude, self.azimuth = altaz[0].degrees, altaz[1].degrees

        self.updateRA(radec[0])
        self.updateDEC(radec[1])

        self.updateAlt(altaz[0])
        self.updateAz(altaz[1])

    def handleInfo(self):
        webbrowser.open(f"https://en.wikipedia.org/wiki/{self.messier}")

    def handleFavorite(self, checked):
        QApplication.instance().databaseManager.updateFavorite(self.pk, TableSelection.MESSIER, checked)


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

    # s = PlanetItem(0, False, "Mercury", "The second planet from the sun", planet)
    barnard = Star(ra_hours=(17, 57, 48.49803),
                   dec_degrees=(4, 41, 36.2072),
                   ra_mas_per_year=-798.71,
                   dec_mas_per_year=10337.77,
                   parallax_mas=545.4,
                   radial_km_per_s=-110.6)
    # s = StarItem(0, True, "Barnard's Star", "The star moving fastest across our sky.", barnard, 9.51, "87937")
    pleiades = Star(ra_hours=(8, 40, 6),
                    dec_degrees=(24, 7, 12))
    # s = MessierItem("The Pleiades", "Messier 45, an open cluster of many blue stars.", pleiades, 1.6, 444, "M45")

    # This TLE might be outdated by the time you're testing this... I'm just using this one for testing.
    # Last Retrieved from Celestrak on 11/29/2023
    line0 = "ISS (ZARYA)"
    line1 = "1 25544U 98067A   23347.97546825  .00010243  00000+0  18476-3 0  9993"
    line2 = "2 25544  51.6397 158.0105 0001827  32.3380 104.5191 15.50377164429678"
    iss = EarthSatellite(line1, line2, line0, ts)
    print(iss)

    s = SatelliteItem(0, True, 'The ISS', "The International Space Station, the largest crewed spacecraft.", iss, "25544")

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