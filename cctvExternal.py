# Additionnal data retrieval from the internet

import location
from http.client import HTTPSConnection
import xml.etree.ElementTree as ET
import math
import commons

# A point of interest (store...)
class Nearby:
    def __init__(self, north=0, east=0, loctype='unknown', name='unknown'):
        self.north = self.lat = north
        self.east = self.lon = east
        self.loctype = loctype
        self.name = name

    def __repr__(self):
        return str(self.north) + "N, " + str(self.east) + "E, " + self.name + ", " + self.loctype
        
# Main class for external requests
class ExternalRequester:
	
    def __init__(self, radius=100.):
        self.radius = radius # Tolerance radius in meter
        return

    # Gives relevant places around a location
    def findCCTVsNearLoc(self, locationN, locationE, radius):
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
            loctype = ''
            name = result.find('name').text#.encode('utf-8')
            for lc in result.findall('type'):
                loctype+='/'+lc.text
            north = result.find('./geometry/location/lat').text
            east = result.find('./geometry/location/lng').text
            aux = Nearby(north, east, loctype, name)
            loc2 = location.Location(float(north),float(east))
            if(commons.dist(loc,loc2) <= 0.001*radius and True):#('atm' in loctype or 'airport' in loctype or 'bank' in loctype or 'city_hall' in loctype or 'embassy' in loctype or 'gas_station' in loctype or 'hospital' in loctype or 'liquor_store' in loctype or 'local_government_office' in loctype or 'police' in loctype or 'post_office' in loctype or 'subway_station' in loctype or 'train_station' in loctype)):
                NearbyLoc.append(aux)
        return NearbyLoc
    
    # Returns all external information available for a path
    def findCCTVsNearPath(self, path):
        # Selects representative points (avoid points too close to each other)
        for i in path:
            for j in path:
                if (i!= j and commons.dist(i,j) < 0.002*self.radius):
                    path.remove(j)
                    extinfo=[]
        for i in path:
            aux = self.findCCTVsNearLoc(i.north, i.east, self.radius)
            extinfo += aux
        return extinfo

# Initializes the externalRequester module
def initExternal(radius = 100.):
    return ExternalRequester(radius)
