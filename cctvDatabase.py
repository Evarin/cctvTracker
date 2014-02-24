# Database part of the project

from location import *
import OSMExtractor
import commons

import sqlite3

# Main class for database work
class CCTVDatabase:
    dbname="cctv.db"

    def __init__(self):
        self.conn = sqlite3.connect(CCTVDatabase.dbname)
        table = "locations"
        c = self.conn.cursor()
        # Checks whether the database already exists
        lc = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+table+"'")
        for row in lc:
            return
        print("INITIALIZATION")
        c.execute("CREATE TABLE locations(north, east, address)")
        c.close()
        self.initData()

    # Initialization of the database with external files
    def initData(self):
        locs1 = OSMExtractor.readFile("openStreetMap.xml")
        locs1 += OSMExtractor.readFile("prefetData.xml")
        self.addCCTVs(locs1)

    # Adding a CCTV into the database
    def addCCTV(self, location):
        c = self.conn.cursor()
        table = "locations"
        c.execute("INSERT INTO "+table+" VALUES (?,?,?)", (location.north, location.east, ""))
        c.close()
        self.conn.commit()
        return

    # Adding a list of CCTVs into the database
    def addCCTVs(self,locations):
        c = self.conn.cursor()
        #print(locations)
        table = "locations"
        places=[(l.north, l.east, "") for l in locations]
        c.executemany("INSERT INTO "+table+" VALUES (?,?,?)", places)
        c.close()
        self.conn.commit()
        return

    # Finding the nearest CCTVS in a radius (tolerance in km)
    def findCCTVs(self, location, tolerance=0.1):
        tolerance /= 10
        c = self.conn.cursor()
        table = "locations"
        locs = c.execute("SELECT * FROM "+table+" WHERE north >= ? AND north <= ? AND east >= ? AND east <= ?",\
                             (location.north-tolerance, location.north+tolerance, location.east-tolerance, location.east+tolerance))
        locations = [Location(row[0], row[1], desc=row[2]) for row in locs]
        locations = [loc for loc in locations if commons.dist(loc, location) <= tolerance*10]
        c.close()
        return locations

    # Updating the database with the human-readable address
    def setAddresses(self, locations):
        c = self.conn.cursor()
        table = "locations"
        places=[(l.desc, l.north, l.east) for l in locations]
        locs = c.executemany("UPDATE "+table+" SET address=? WHERE north=? AND east=?", places)
        c.close()
        self.conn.commit()

# Just inits a connection with the database
def initDatabase():
    return CCTVDatabase()
