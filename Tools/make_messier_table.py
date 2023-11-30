import sqlite3
import pandas

connection = sqlite3.connect("../nightsky.db")

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS messier_objects")

cursor.execute("CREATE TABLE messier_objects(" \
        "pk INTEGER PRIMARY KEY AUTOINCREMENT," \
        "favorited INTEGER," \
        "m TEXT," \
        "alt_name TEXT," \
        "type TEXT," \
        "mag REAL," \
        "ra REAL," \
        "dec REAL," \
        "con TEXT," \
        "size_x REAL," \
        "size_y REAL," \
        "dist REAL," \
        "search_text TEXT)")

df = pandas.read_csv("../Messier Catalog.tsv", sep="\t")

def parse_size(size):
    l = size.split("x")
    if len(l) > 1:
        return (float(l[0]), float(l[1]))
    else:
        return (float(l[0]), float(l[0]))

def parse_ra(ra):
    s = ra.split("h")
    h = float(s[0]) * 360.0/24.0
    m = float(s[1].replace("m", "")) * 15.0/60.0
    return h + m

def parse_dec(dec):
    is_negative = dec.startswith("-")
    s = dec.split("°")
    deg = float(s[0])
    m = float(s[1]) / 60.0

    return deg + m * (-1.0 if is_negative else 1.0)
    
for index, row in df.iterrows():
    favorited = False
    m = row["M"]
    alt_name = row["NGC"] if "NGC" not in row["NGC"] else ' '.join(row["NGC"].split(' ')[2:])

    if alt_name == '':
        alt_name = f"Messier {m[1:]}"

    feature_type = row["TYPE"]
    constellation = row["CONS"]
    ra = parse_ra(row["RA"])
    dec = parse_dec(row["DEC"])
    mag = float(row["MAG"])
    sizex, sizey = parse_size(row["SIZE"])
    dist = float(row["DIST (ly)"].replace(",", ""))
    search_text = f"Messier {m} {row['NGC']} {feature_type} {constellation}"

    data = (favorited, m, alt_name, feature_type, mag, ra, dec, constellation, sizex, sizey, dist, search_text)

    cursor.execute(
        "INSERT INTO messier_objects (favorited, m, alt_name, type, mag, ra, dec, con, size_x, size_y, dist, search_text) " \
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        data)


connection.commit()
