# Data structure for locations
# Data processing of Google Location History
from xml.dom.minidom import parseString

# Data structure
class Location:
    def __init__(self, lat, lon, time=0):
        self.north = self.lat = lat
        self.east = self.lon = lon
        self.time = time

    def __repr__(self):
        return str(self.lat) + "N, " + str(self.lon) + "E"

# Data processing
def locationHistory(filename):

    myLocation = []

    # reads KML file as a string
    file = open(filename)
    data = file.read()
    file.close()

    # parses string into DOM
    dom = parseString(data)

    # retrieves coordinates, whatever the namespace
    for d in dom.getElementsByTagNameNS('*','coord'):
        #in kml doc, first is longitude and second is latitude
        coords=d.firstChild.data.split(' ')
        x=Location(float(coords[1]),float(coords[0]))
        myLocation.append(x)
    return myLocation
