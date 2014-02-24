import cctvDatabase
import cctvExternal
from location import *
import mapsDisplayer
import sys
import webbrowser

mainDB = cctvDatabase.initDatabase()
extDB = cctvExternal.initExternal(50)

def findCCTVs(locations):
    cctv = []
    for loc in locations:
        cctv += mainDB.findCCTVs(loc)
    print(len(cctv))
    extcctv = extDB.findCCTVsNearPath(locations)
    return (cctv, extcctv)

if len(sys.argv)<2:
    print("usage: python3 "+sys.argv[0]+" nom_du_fichier.kml")
else:
    locfile = sys.argv[1]
    locations = locationHistory(locfile)
    res, eres = findCCTVs(locations)

    ofile = open("report.html","w")
    ofile.write(mapsDisplayer.exportHTML(locations, res, eres, mainDB))
    ofile.close()
    
    try:
        webbrowser.open("report.html")
    except Exception:
        print("end")
