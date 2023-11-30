import sqlite3

connection = sqlite3.connect("../nightsky.db")

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS solarsystem_objects")

cursor.execute("CREATE TABLE solarsystem_objects(" \
        "pk INTEGER PRIMARY KEY AUTOINCREMENT," \
        "favorited INTEGER," \
        "ephemeris TEXT," \
        "name TEXT," \
        "ephemeris_key TEXT," \
        "search_text TEXT)")

#JPL Ephemeris de421 keys
de421 = [
    ["Mercury", "Mercury", "mercury"],
    ["Venus", "Venus", "venus"],
    ["Earth", "Earth", "earth"],
    ["The Moon", "Moon", "the moon luna"],
    ["Mars", "Mars", "mars"],
    ["Jupiter Barycenter", "Jupiter", "jupiter"],
    ["Saturn Barycenter", "Saturn", "saturn"],
    ["Uranus Barycenter", "Uranus", "uranus"],
    ["Neptune Barycenter", "Neptune", "neptune"],
    ["Pluto Barycenter", "Pluto", "134340 pluto"],
    ["The Sun (Sol)", "Sun", "the sun sol g2v"],
]

for key in de421:
    data = (False, "de421.bsp", key[1], key[0], key[2])
    cursor.execute("INSERT INTO solarsystem_objects (favorited, ephemeris, name, ephemeris_key, search_text) VALUES (?, ?, ?, ?, ?)", data)

connection.commit()