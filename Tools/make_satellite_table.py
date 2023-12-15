import sqlite3
import time
import math

from skyfield.api import load, EarthSatellite

from Utils.utils import get_satellite_tle

connection = sqlite3.connect("../nightsky.db")

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS satellite_objects")

cursor.execute("CREATE TABLE satellite_objects(" \
        "pk INTEGER PRIMARY KEY AUTOINCREMENT," \
        "favorited INTEGER," \
        "norad_id TEXT," \
        "name TEXT," \
        "desc TEXT," \
        "tle TEXT," \
        "refresh_time INTEGER,"\
        "decayed INTEGER," \
        "search_text TEXT)")

base_satellites = [
    ("International Space Station", "The largest crewed spacecraft, launched with international cooperation in 1998.", 25544),
    ("ISS Tool Bag", "Toolbag lost while on a spacewalk.", 58229),
    ("Tiangong Space Station", "Space station operated by China, launched in 2021.", 48274),
    ("Hubble Space Telescope", "Space telescope operated by NASA.", 20580),
    ("Mir Space Station", "Russian space station deorbited in 2001.", 16609),
    ("Starlink-46", "Deorbited in 2020.", 44246),
    ("Starlink-5226", "Satellite of the Starlink constellation.", 54056),
    ("Lemur 2 Miriwari", "Cubesat of the Lemur 2 constellation.", 51054),
    ("Lemur 2 SarahBettyBoo", "Cubesat of the Lemur 2 Constellation.", 43888)
]

ts = load.timescale()
t = ts.now()

for satellite in base_satellites:

    decayed = False
    try:
        print(f"Getting Norad ID {satellite[2]}", end="")
        line0, line1, line2, tle = get_satellite_tle(satellite[2])
        sat = EarthSatellite(line1, line2, line0, ts)
        geocentric = sat.at(t)
        if math.isnan(geocentric.position.km[0]):
            decayed = True
    except ConnectionError:
        print("Skipping...")
        continue
    except IndexError:
        tle = ""
        decayed = True



    if decayed:
        print(" DECAYED")
    else:
        print("")

    search_text = ' '.join([satellite[0].lower(), satellite[1].lower(), str(satellite[2])])
    data = (True, satellite[2], satellite[0], satellite[1], tle, int(time.time()), decayed, search_text)

    sql = "INSERT INTO satellite_objects (favorited, norad_id, name, desc, tle, refresh_time, decayed, search_text)" \
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    cursor.execute(sql, data)

connection.commit()
