# Insertion dans la base de donnees
# Requetes sur la base

from location import *
import OSMExtractor
import commons

import sqlite3

class CCTVDatabase:
    dbname="cctv.db"

    def __init__(self):
        self.conn = sqlite3.connect(CCTVDatabase.dbname)
        table = "locations"
        c = self.conn.cursor()
        # Regarde si une base de donnees SQL a deja ete creee
        lc = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+table+"'")
        for row in lc:
            return
        print("INITIALIZATION")
        c.execute("CREATE TABLE locations(north, east, address)")
        c.close()
        self.initData()

    def addCCTV(self, location):
        c = self.conn.cursor()
        table = "locations"
        c.execute("INSERT INTO "+table+" VALUES (?,?,?)", (location.north, location.east, ""))
        c.close()
        self.conn.commit()
        return

    def addCCTVs(self,locations):
        c = self.conn.cursor()
        #print(locations)
        table = "locations"
        places=[(l.north, l.east, "") for l in locations]
        c.executemany("INSERT INTO "+table+" VALUES (?,?,?)", places)
        c.close()
        self.conn.commit()
        return

    def findCCTVs(self, location, tolerance=0.01):
        c = self.conn.cursor()
        table = "locations"
        locs = c.execute("SELECT * FROM "+table+" WHERE north >= ? AND north <= ? AND east >= ? AND east <= ?",\
                             (location.north-tolerance, location.north+tolerance, location.east-tolerance, location.east+tolerance))
        locations = [Location(row[0], row[1]) for row in locs]
        locations = [loc for loc in locations if commons.dist(loc, location) <= tolerance*10]
        c.close()
        return locations
    
    def setAddress(self, locations):
        c = self.conn.cursor()
        table = "locations"
        locs = c.execute("SELECT * FROM "+table+" WHERE north >= ? AND north <= ? AND east >= ? AND east <= ?",\
                             (location.north-tolerance, location.north+tolerance, location.east-tolerance, location.east+tolerance))
        locations = [Location(row[0], row[1]) for row in locs]
        locations = [loc for loc in locations if commons.dist(loc, location) <= tolerance*10]
        c.close()
    
    def initData(self):
        locs1 = OSMExtractor.readFile("openStreetMap.xml")
        locs1 += OSMExtractor.readFile("prefetData.xml")
        self.addCCTVs(locs1)

def initDatabase():
    return CCTVDatabase()
