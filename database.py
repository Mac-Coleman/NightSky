# This Python file uses the following encoding: utf-8
import sqlite3
from objects import MessierObject, SolarSystemObject

from enum import Enum

class TableSelection(Enum):
    SATELLITE = 1
    SOLAR_SYSTEM = 2
    STAR = 3
    MESSIER = 4

from object_widgets import ObjectCard

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

        terms_corrected = ('%' + '%'.join(term.split(' ')) + '%',)
        rows = self.cursor.execute(
            sql,
            terms_corrected
        )

        def make_card(solarsystemObject):
            return ObjectCard(solarsystemObject[3], solarsystemObject[0], solarsystemObject[1], TableSelection.SOLAR_SYSTEM)
        
        return map(make_card, rows)
    
    def searchSatellites(self, term: str, favorited: bool) -> list[ObjectCard]:
        pass

    def searchStars(self, term: str, favorited: bool) -> list[ObjectCard]:
        sql = "SELECT * FROM hipparcos_objects WHERE search_text LIKE ?"

        if favorited:
            sql += " AND favorited = TRUE"

        terms_corrected = ('%' + '%'.join(term.split(' ')) + '%',)
        rows = self.cursor.execute(
            sql,
            terms_corrected
            )
        
        def make_card(star):
            return ObjectCard(star[10], star[0], star[1], TableSelection.STAR)
        
        return map(make_card, rows)
    
    def searchMessier(self, term: str, favorited: bool) -> list[ObjectCard]:
        sql = "SELECT * FROM messier_objects WHERE search_text LIKE ?"

        if favorited:
            sql += " AND favorited = TRUE"

        terms_corrected = ('%' + '%'.join(term.split(' ')) + '%',)
        rows = self.cursor.execute(
            sql,
            terms_corrected
        )

        def make_card(messier_object):
            return ObjectCard(messier_object[3], messier_object[0], messier_object[1], TableSelection.MESSIER)

        return map(make_card, rows)
    
    def updateFavorite(self, pk: int, table: TableSelection, favorited: bool) -> None:

        table_name = None

        match table:
            case TableSelection.SATELLITE:
                table_name = 'satellites'
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




# if __name__ == "__main__":
#     pass
