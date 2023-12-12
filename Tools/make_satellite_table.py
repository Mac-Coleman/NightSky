import sqlite3
from skyfield.api import Loader

load = Loader('/dev/null')

connection = sqlite3.connect("../nightsky.db")

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS satellite_objects")

cursor.execute("CREATE TABLE satellite_objects(" \
        "pk INTEGER PRIMARY KEY AUTOINCREMENT," \
        "favorited INTEGER," \
        "norad_id TEXT," \
        "name TEXT," \
        "tle TEXT," \
        "refresh_time INTEGER,"\
        "search_text TEXT)")

base_satellites = [
    ("International Space Station", "The largest crewed spacecraft, launched with international cooperation in 1998.", 25544),
    ("ISS Tool Bag", "Toolbag lost while on a spacewalk.", 58229),
    ("Tiangong Space Station", "Space station operated by China, launched in 2021.", 48274),
    ("Hubble Space Telescope", "Space telescope operated by NASA.", 20580)
]

for satellite in base_satellites:
