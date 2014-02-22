import cctvDatabase
import cctvExternal
from location import *

mainDB = cctvDatabase.initDatabase()
extDB = cctvExternal.initExternal()

def findCCTVs(location):
    cctv1 = mainDB.findCCTVs(location)
    cctv2 = []#extDB.findCCTVs(location)
    return cctv1 + cctv2

locations = findMyLocation("history-02-20-2014.kml")
res = findCCTVs(Location(48.846597, 2.345231))
print(res)
