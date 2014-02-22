# Traitement du fichier OpenStreetMap.XML
from location import *

from xml.dom.minidom import parseString

def readFile(filename):
    locations = []

    # read XML file as a string
    file = open(filename)
    data = file.read()
    file.close()

    # parse string into DOM
    dom = parseString(data)

    # retrieve coordinates
    for d in dom.getElementsByTagName('node'):
        x = Location(float(d.getAttribute("lat")),float(d.getAttribute("lon")))
        locations.append(x)
    return locations
