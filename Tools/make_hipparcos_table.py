import sqlite3
import pandas
from skyfield.api import load
from skyfield.data import hipparcos

connection = sqlite3.connect("../nightsky.db")

cursor = connection.cursor()

# Star Values and Columns
# This is a list of fields for Skyfield Star objects and their columns within the hipparcos table.

# Right ascension hours: H3 (RA)
# Declination degrees: H9 (Dec_Deg)
# Right ascension milliarcseconds per year: H12 (pm_RA)
# Declination milliarcseconds per year: H13 (pm_Dec)
# Parallax milliarcseconds: H11 (Plx)
# Radial kilometers per second: Skip
# names: Name
# epoch: J1991.25

# https://heasarc.gsfc.nasa.gov/w3browse/all/hipparcos.html

# This is where I will need to transfer the columns of this dataset into the database.
# Also, add a favorited column, probably? This is a bit difficult, hmm.

cursor.execute("DROP TABLE IF EXISTS hipparcos_objects")

# TRUE and FALSE are literals mapped to 0 and 1. No Boolean datatypes in SQLite3.
cursor.execute("CREATE TABLE hipparcos_objects(" \
        "pk INTEGER PRIMARY KEY AUTOINCREMENT," \
        "favorited INTEGER," \
        "hip TEXT," \
        "ra REAL," \
        "dec REAL," \
        "pmra REAL," \
        "pmdec REAL," \
        "plx REAL," \
        "ap_mag REAL," \
        "spec_type TEXT," \
        "common_name TEXT," \
        "search_text TEXT)")

# Build map of common star names
common_table = pandas.read_csv("ident6.doc", sep="|", header=None)

common_names = {}

for index, row in common_table.iterrows():
    common_names[str(row[1])] = row[0].strip()

load.open(hipparcos.URL, filename="../hip_main.dat")
df = pandas.read_csv("../hip_main.dat", sep="|", header=None)

count = 0
for index, row in df.iterrows():
    if str(row[8]).strip() == "" or str(row[9]).strip() == "" or str(row[5]) == "":
        continue

    if float(row[5]) > 10:
        continue

    favorited = False
    hip = str(row[1]).strip()
    ra = float(row[8])
    dec = float(row[9])
    pmra = float(row[12])
    pmdec = float(row[13])
    plx = float(row[11])
    ap_mag = float(row[5])
    spec_type = str(row[76]).strip()
    common_name = common_names.get(hip, "HIP " + hip)
    search_text = hip + " " + spec_type + " " + common_name

    data = (favorited, hip, ra, dec, pmra, pmdec, plx, ap_mag, spec_type, common_name, search_text)

    count += 1

    cursor.execute(
        "INSERT INTO hipparcos_objects(favorited, hip, ra, dec, pmra, pmdec, plx, ap_mag, spec_type, common_name, search_text) VALUES " \
        "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        data
    )

connection.commit()

print(f"Inserted {count} stars into the database.")