import cctvDatabase
import cctvExternal
from location import *
import mapsDisplayer

mainDB = cctvDatabase.initDatabase()
extDB = cctvExternal.initExternal()

def findCCTVs(locations):
    cctv = []
    for loc in locations:
        cctv += mainDB.findCCTVs(loc)
    #cctv2 = extDB.findCCTVs(locations)
    return cctv# + cctv2

locations = findMyLocation("history-02-20-2014.kml")
res = findCCTVs(locations)

ofile = open("result.html","w")
ofile.write(mapsDisplayer.exportHTML(locations, res))
ofile.close()
print()
