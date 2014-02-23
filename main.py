import cctvDatabase
import cctvExternal
from location import *
import mapsDisplayer

mainDB = cctvDatabase.initDatabase()
#extDB = cctvExternal.initExternal()

def findCCTVs(locations):
    cctv = []
    for loc in locations:
        cctv += mainDB.findCCTVs(loc)
    print(len(cctv))
    extcctv = cctvExternal.queryExternal(locations, 10)
    return (cctv, extcctv)

locations = locationHistory('LocationHistory/history-02-22-2014.kml')
res, eres = findCCTVs(locations)

ofile = open("result.html","w")
ofile.write(mapsDisplayer.exportHTML(locations, res, eres))
ofile.close()
print()
