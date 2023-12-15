# This Python file uses the following encoding: utf-8
from enum import Enum
import sqlite3
import time
import math

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from skyfield.api import Star, EarthSatellite



from objects import MessierObject, SolarSystemObject

class TableSelection(Enum):
    SATELLITE = 1
    SOLAR_SYSTEM = 2
    STAR = 3
    MESSIER = 4

from Search_Item.SearchItem import SatelliteItem, PlanetItem, StarItem, MessierItem

from object_widgets import ObjectCard
from Utils.utils import get_satellite_tle

class DatabaseManager(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.connection = sqlite3.connect("nightsky.db")
        self.cursor = self.connection.cursor()

    def getMessierObjects(self) -> list[MessierObject]:
        rows = self.cursor.execute("SELECT * FROM messier_objects")

        output = []

        for r in rows:
            c = MessierObject(r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10])
            output.append(c)

        return output
    
    def getSolarSystemObjects(self) -> list[SolarSystemObject]:
        rows = self.cursor.execute("SELECT * FROM solarsystem_objects")

        output = []

        for r in rows:
            c = SolarSystemObject(r[1], r[2], r[3], r[4], r[5])
            output.append(c)
        
        return output
    
    def searchSolarSystem(self, term: str, favorited: bool) -> list[ObjectCard]:
        sql = "SELECT * FROM solarsystem_objects WHERE search_text LIKE ?"

        if favorited:
            sql += " AND favorited = TRUE"
        else:
            sql += " LIMIT 10"

        terms_corrected = ('%' + '%'.join(term.split(' ')) + '%',)
        rows = self.cursor.execute(
            sql,
            terms_corrected
        )

        def make_card(solarsystem_object):
            i = PlanetItem(solarsystem_object[0], solarsystem_object[1], solarsystem_object[3], "Null", QApplication.instance().ephemeris[solarsystem_object[4]])
            i.updatePosition()
            return i
        
        return map(make_card, rows)

    def searchSatellites(self, term: str, favorited: bool) -> list[SatelliteItem]:
        sql = "SELECT * FROM satellite_objects WHERE search_text LIKE ?"

        if favorited:
            sql += " AND favorited = TRUE"
        else:
            sql += " LIMIT 10"

        terms_corrected = ('%' + '%'.join(term.split(' ')) + '%',)
        rows = self.cursor.execute(
            sql,
            terms_corrected
        )

        def make_card(satellite):
            # return ObjectCard(star[10], star[0], star[1], TableSelection.STAR)
            s = None
            if satellite[5] != "":
                line0, line1, line2, *_ = satellite[5].split("\n")
                s = EarthSatellite(line1, line2, line0, QApplication.instance().timescale)

            i = SatelliteItem(satellite[0], satellite[1], satellite[3], satellite[4], s, satellite[2])
            i.updatePosition()
            return i

        return list(map(make_card, rows))

    def searchStars(self, term: str, favorited: bool) -> list[ObjectCard]:
        sql = "SELECT * FROM hipparcos_objects WHERE search_text LIKE ?"

        if favorited:
            sql += " AND favorited = TRUE"
        else:
            sql += " LIMIT 10"

        terms_corrected = ('%' + '%'.join(term.split(' ')) + '%',)
        rows = self.cursor.execute(
            sql,
            terms_corrected
            )

        
        def make_card(star):
            # return ObjectCard(star[10], star[0], star[1], TableSelection.STAR)
            s = Star(ra_hours=star[3], dec_degrees=star[4], ra_mas_per_year=star[5], dec_mas_per_year=star[6], parallax_mas=star[7])
            i = StarItem(star[0], star[1], star[10], f"A {star[9]} star", s, star[8], star[2])
            i.updatePosition()
            return i
        
        return map(make_card, rows)
    
    def searchMessier(self, term: str, favorited: bool) -> list[ObjectCard]:
        sql = "SELECT * FROM messier_objects WHERE search_text LIKE ?"

        if favorited:
            sql += " AND favorited = TRUE"
        else:
            sql += " LIMIT 10"

        terms_corrected = ('%' + '%'.join(term.split(' ')) + '%',)
        rows = self.cursor.execute(
            sql,
            terms_corrected
        )

        def make_card(messier_object):
            s = Star(ra_hours=messier_object[6], dec_degrees=messier_object[7])
            i = MessierItem(messier_object[0], messier_object[1], messier_object[3], messier_object[4], s, messier_object[5], messier_object[11], messier_object[2])
            i.updatePosition()
            return i

        return map(make_card, rows)
    
    def updateFavorite(self, pk: int, table: TableSelection, favorited: bool) -> None:

        table_name = None

        match table:
            case TableSelection.SATELLITE:
                table_name = 'satellite_objects'
            case TableSelection.SOLAR_SYSTEM:
                table_name = "solarsystem_objects"
            case TableSelection.STAR:
                table_name = 'hipparcos_objects'
            case TableSelection.MESSIER:
                table_name = 'messier_objects'
            case _:
                return

        # BAD
        sql = f"UPDATE {table_name} SET favorited = ? WHERE pk = ?"

        data = (favorited, pk)

        self.cursor.execute(
            sql,
            data
        )

        self.connection.commit()

    def getBrightStars(self):
        sql = 'SELECT pk, ra, dec, ap_mag, common_name FROM hipparcos_objects WHERE ap_mag < 5.0'
        rows = self.cursor.execute(sql)
        return list(rows)
        # test
        # s = []
        # for i in range (0, 360, 10):
        #     for j in range(-90, 90, 10):
        #         s.append([i * 180 + j, i, j, 5])
        # return s

    def getAllSatellites(self):
        sql = 'SELECT * FROM satellite_objects'
        rows = self.cursor.execute(sql)
        return list(rows)

    def addSatellite(self, name, desc, id):
        sql = "INSERT INTO satellite_objects (favorited, norad_id, name, desc, tle, refresh_time, decayed, search_text)" \
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

        try:
            _, _, _, tle = get_satellite_tle(id)
        except ConnectionError:
            raise ValueError(f"{id} could not be retrieved.")
        except ValueError:
            raise ValueError(f"{id} could not be retrieved.")
        except IndexError:
            raise ValueError(f"{id} could not be retrieved.")

        data = (0, id, name, desc, tle, int(time.time()), False, ' '.join([name.lower(), desc.lower(), id]))

        self.cursor.execute(sql, data)
        self.connection.commit()

    def refreshOutOfDate(self):
        fetch = "SELECT pk, norad_id FROM satellite_objects WHERE refresh_time < ?"
        data = (int(time.time()) - 60*60*24*2,)  # The comma is needed to recognize it as a tuple.

        rows = list(self.cursor.execute(fetch, data))

        for sat in rows:
            try:
                _, _, _, tle = get_satellite_tle(sat[1])
            except ConnectionError:
                raise ValueError(f"{id} could not be retrieved.")
            except ValueError:
                raise ValueError(f"{id} could not be retrieved.")
            except IndexError:
                raise ValueError(f"{id} could not be retrieved.")

            update = "UPDATE satellite_objects SET tle = ?, refresh_time = ? WHERE pk IS ?"
            data = (tle, int(time.time()), sat[0])

            self.cursor.execute(update, data)

        self.connection.commit()

    def refreshAll(self):
        fetch = "SELECT pk, norad_id FROM satellite_objects"

        rows = list(self.cursor.execute(fetch))

        for sat in rows:
            try:
                _, _, _, tle = get_satellite_tle(sat[1])
            except ConnectionError:
                continue
            except ValueError:
                continue
            except IndexError:
                continue

            update = "UPDATE satellite_objects SET tle = ?, refresh_time = ? WHERE pk IS ?"
            data = (tle, int(time.time()), sat[0])

            self.cursor.execute(update, data)

        self.connection.commit()

    def deleteSatellite(self, pk):
        delete = "DELETE FROM satellite_objects WHERE pk = ?"
        data = (pk,)

        self.cursor.execute(delete, data)
        self.connection.commit()

    def deleteDecayed(self):
        fetch = "SELECT * FROM satellite_objects"
        rows = list(self.cursor.execute(fetch))

        for sat in rows:
            print("Decayed:", sat[7], "TLE:", sat[5])
            if sat[7] == 1 or sat[5] == "":
                self.deleteSatellite(sat[0])
                continue

            line0, line1, line2, *_ = sat[5].split("\n")
            s = EarthSatellite(line1, line2, line0, QApplication.instance().timescale)
            geocentric = s.at(QApplication.instance().skyTime)
            if math.isnan(geocentric.position.km[0]):
                self.deleteSatellite(sat[0])






# if __name__ == "__main__":
#     pass
