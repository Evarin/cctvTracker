# Recherche de donnees supplementaires sur internet

import location
#replace hhtp.client with httplib; don't forget to change it back
import httplib
import xml.etree.ElementTree as ET
import math

class Nearby:
    def __init__(self, north=0, east=0, loctype='unknown', name='unknown'):
        self.north=north
        self.east=east
        self.loctype=loctype
        self.name=name

    def __repr__(self):
        return str(self.north) + "N, " + str(self.east) + "E, " + self.name + ", " + self.loctype
        
class ExternalRequester:
    googleAPIKey = "AIzaSyAQbUKKDk_G0y51l0BTiFP282hcbanlKs4"
    #alternative key: "AIzaSyChH08xskE0kNH_Ih9oO08wpK2LzYf9x5Y"
    
	
    def __init__(self, googleAPIKey):
        self.googleAPIKey=googleAPIKey

    def findCCTVs(self, locationN, locationE, radius):
        NearbyLoc = []
        conn = httplib.HTTPSConnection("maps.googleapis.com")
        parametres = "location="+str(locationN)+","+str(locationE)+"&radius="+str(radius)+"&sensor=false&key="+ExternalRequester.googleAPIKey
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
            NearbyLoc.append(aux)
        return NearbyLoc

#compute distance between two locations

def dist(loc1,loc2):
    degrees_to_radians = math.pi/180.0
    phi1 = (90.0 - loc1.north)*degrees_to_radians
    phi2 = (90.0 - loc2.north)*degrees_to_radians
    theta1 = loc1.east*degrees_to_radians
    theta2 = loc2.east*degrees_to_radians
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    #distance in km
    arc = arc * 6373
    return arc

#return all external information available for a file
def initExternal(key,filename,radius):
    db = ExternalRequester(key)
    path = location.findMyLocation(filename)
    #select representative points (avoid points too close to each other)
    for i in path:
        for j in path:
            if (i!= j and dist(i,j)< 0.002*radius):
                path.remove(j)
    extinfo=[]
    for i in path:
        aux=db.findCCTVs(i.north,i.east,radius)
        extinfo = list(set(extinfo+aux))
    return extinfo

res=initExternal("AIzaSyChH08xskE0kNH_Ih9oO08wpK2LzYf9x5Y",'LocationHistory/history-02-22-2014.kml',100)
