# Recherche de donnees supplementaires sur internet

import location
#replace hhtp.client with httplib; don't forget to change it back
from http.client import HTTPSConnection
import xml.etree.ElementTree as ET
import math
import commons

class Nearby:
    def __init__(self, north=0, east=0, loctype='unknown', name='unknown'):
        self.north=north
        self.east=east
        self.loctype=loctype
        self.name=name

    def __repr__(self):
        return str(self.north) + "N, " + str(self.east) + "E, " + self.name + ", " + self.loctype
        
class ExternalRequester:
	
    def __init__(self):
        return

    def findCCTVs(self, locationN, locationE, radius):
        print("Google Query")
        loc=location.Location(float(locationN),float(locationE))
        NearbyLoc = []
        conn = HTTPSConnection("maps.googleapis.com")
        parametres = "location="+str(locationN)+","+str(locationE)+"&radius="+str(radius)+"&sensor=false&key="+commons.googleAPIKey
        conn.request("GET", "/maps/api/place/nearbysearch/xml?"+parametres)
        response = conn.getresponse()
        data = response.read()
        root = ET.fromstring(data)
        for result in root.findall('result'):
            loctype=''
            name=result.find('name').text.encode('utf-8')
            for lc in result.findall('type'):
                loctype+='/'+lc.text
            north = result.find('./geometry/location/lat').text
            east = result.find('./geometry/location/lng').text
            aux=Nearby(north,east,loctype,name)
            loc2=location.Location(float(north),float(east))
            if(commons.dist(loc,loc2) <= 0.001*radius and ('atm' in loctype or 'airport' in loctype or 'bank' in loctype or 'city_hall' in loctype or 'embassy' in loctype or 'gas_station' in loctype or 'hospital' in loctype or 'liquor_store' in loctype or 'local_government_office' in loctype or 'police' in loctype or 'post_office' in loctype or 'subway_station' in loctype or 'train_station' in loctype)):
                NearbyLoc.append(aux)
        return NearbyLoc

#return all external information available for a file
def queryExternal(path, radius):
    db = ExternalRequester()
    #select representative points (avoid points too close to each other)
    for i in path:
        for j in path:
            if (i!= j and commons.dist(i,j)< 0.002*radius):
                path.remove(j)
    extinfo=[]
    for i in path:
        aux=db.findCCTVs(i.north,i.east,radius)
        extinfo = ((extinfo+aux))
    return extinfo

#res=initExternal("AIzaSyChH08xskE0kNH_Ih9oO08wpK2LzYf9x5Y",'LocationHistory/history-02-22-2014.kml',100)
