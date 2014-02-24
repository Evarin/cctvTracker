# Data structure for locations
# Data processing of Google Location History

from xml.dom.minidom import parseString
from xml.dom.minidom import Node

# Data structure
class Location:
    def __init__(self, lat, lon, time=0, desc=""):
        self.north = self.lat = lat
        self.east = self.lon = lon
        self.time = time
        self.desc = desc

    def __repr__(self):
        return str(self.lat) + "N, " + str(self.lon) + "E"
    
    def latlng(self):
        return str(self.lat) + "," + str(self.lon)

# Data processing
def locationHistory(filename):

    myLocation = []

    # reads KML file as a string
    file = open(filename)
    data = file.read()
    file.close()

    # parses string into DOM
    dom = parseString(data)
    time = ""

    # retrieves coordinates, whatever the namespace
    for track in dom.getElementsByTagNameNS("*", 'Track'):
        for d in track.childNodes:
            if d.nodeType != Node.ELEMENT_NODE:
                continue
            if d.tagName == "when":
                time = d.firstChild.data
            if d.tagName == "gx:coord":
                #in kml doc, first is longitude and second is latitude
                coords = d.firstChild.data.split(' ')
                x = Location(float(coords[1]), float(coords[0]), time)
                myLocation.append(x)
            
    return myLocation
