# Structure de donnees et extraction des coordonnees GPS / KML

class Location:
    
    def __init__(self, north=0, east=0):
        self.north=north
        self.east=east

    def __repr__(self):
        return str(self.north) + "N, " + str(self.east) + "E"



from xml.dom.minidom import parseString

def findMyLocation(location):

    myLocation= []

    #read KML file as a string
    file = open(location)
    data = file.read()
    file.close()

    #parse string into DOM
    dom = parseString(data)

    #retrieve coordinates, whatever the namespace
    for d in dom.getElementsByTagNameNS('*','coord'):
        #in kml doc, first is longitude and second is latitude
        coords=d.firstChild.data.split(' ')
        x=Location(float(coords[1]),float(coords[0]))
        myLocation.append(x)
    return myLocation
