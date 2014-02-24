# Output functions

import commons

from http.client import HTTPSConnection
from xml.dom.minidom import parseString
from datetime import datetime
from location import *

# Main html generator

def exportHTML(path, cctv, ecctv, db):
    # Double apparition elimination
    cctv = [Location(n, e, desc=d) for (n, e, d) in \
                set([(loc.north, loc.east, loc.desc) for loc in cctv]) ]
    rawCCTV = []
    toupdate = []
    for loc in cctv:
        if loc.desc == "":
            lookForAddress(loc)
            toupdate+=[loc]
        minloc = path[0]
        mindist = 100000
        for p in path:
            dst = commons.dist(loc, p)
            if dst<mindist:
                minloc = p
                mindist = dst
        loc.time = minloc.time
        rawCCTV.append((loc, mindist))
    stores = []

    db.setAddresses(toupdate)

    ecctv = [Location(n, e, desc=d) for (n, e, d) in \
                 set([(float(loc.north), float(loc.east), str(loc.name)) for loc in ecctv]) ]
    for loc in ecctv:
        minloc = path[0]
        mindist = 100000
        for p in path:
            dst = commons.dist(loc, p)
            if dst<mindist:
                minloc = p
                mindist = dst
        loc.time = minloc.time
        stores.append((loc, mindist))

    # Rendering
    (head1, body1) = makeMapView(path, rawCCTV, stores)
    (head2, body2) = makeReport(path, rawCCTV, stores)

    output = "<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n <title>Smile, you're on TV</title>\n "\
        + head1 + "\n\
 <style type=\"text/css\">\n html { height: 100% }\n body { height: 100%; margin: 0; padding: 0 }\n #map-canvas { height: 100%; width: 48%; float:left }\n #report { width:48%; float:right; height: 100%; overflow: auto}\n li{margin-top:10px;}</style>\n\
 </head>\n\n<body>"+body1+"<div id=\"report\">\n"+body2+"\n</div>\n\
 </body>\n</html>"
    return output

def dist2str(dist):
    # Distance en km
    if dist<1:
        return str(round(dist*1000))+"m"
    else:
        return str(round(dist*10)/10)+"km"

# Finds the address of a location via Google
def lookForAddress(loc):
    print("Google GEOCODE Query")
    conn = HTTPSConnection("maps.googleapis.com")
    parametres = "latlng="+loc.latlng()+"&sensor=false&key="+commons.googleAPIKey
    conn.request("GET", "/maps/api/geocode/xml?"+parametres)
    response = conn.getresponse()
    data = response.read()
    dom = parseString(data)
    for d in dom.getElementsByTagNameNS("*", 'formatted_address'):
         loc.desc = d.firstChild.data
         return

def date2human(tme):
    tme=tme.split(".")[0]
    date = datetime.strptime(tme, "%Y-%m-%dT%H:%M:%S")
    return "le "+date.strftime("%d %a %Y") +" à "+date.strftime("%H:%M")

# Makes a report of what's relevant
# Saves CCTV addresses in database if unknown
def makeReport(path, cctv, ecctv):
    output = "<h1>Rapport de passage à la (CC)TV</h1>\n <ul>\n"
    for (loc, dist) in cctv:
        output += "  <li itemscope itemtype=\"http://schema.org/Place\"><meta itemprop=\"latitude\" content=\""+str(loc.north)+"\" /><meta itemprop=\"longitude\" content=\""+str(loc.east)+"\" />\
Caméra publique à l'adresse "+loc.desc+"<br />Passage à "+dist2str(dist)+" "+date2human(loc.time)+"</li>\n"
    for (loc, dist) in ecctv:
        output += "  <li itemscope itemtype=\"http://schema.org/Place\"><meta itemprop=\"latitude\" content=\""+str(loc.north)+"\" /><meta itemprop=\"longitude\" content=\""+str(loc.east)+"\" />\
Autre lieu : "+loc.desc+"<br />Passage à "+dist2str(dist)+" "+date2human(loc.time)+"</li>\n"
    output+="</ul>\n"
    return ("", output)

def addslashes(txt):
    return txt.replace('\'','\\\'',-1)

def makeMapView(path, cctv, ecctv):
    pcoords = ""
    ecoords = ""
    ccoords = ""
    centern = 0.
    centere = 0.

    # Chemin utilisateur
    for loc in path:
        pcoords += "new google.maps.LatLng("+str(loc.north)+", "+str(loc.east)+"),\n"
        centern += loc.north
        centere += loc.east
    pcoords = pcoords[:-2]
    centern /= max(1, len(path))
    centere /= max(1, len(path))

    for (loc, dist) in cctv:
        ccoords += "new google.maps.Marker({ position: new google.maps.LatLng("+loc.latlng()+"),\
 map: map, title: '"+addslashes(loc.desc)+"', icon: cctvIcon});\n";
    
    for (loc, dist) in ecctv:
        ecoords += "new google.maps.Marker({ position: new google.maps.LatLng("+loc.latlng()+"),\
 map: map, title: '"+addslashes(loc.desc)+"'});\n";

    js = "<meta name=\"viewport\" content=\"initial-scale=1.0, user-scalable=yes\" />\n\
 <script type=\"text/javascript\" src=\"https://maps.googleapis.com/maps/api/js?key="+commons.googleAPIKey+"&sensor=false\"></script>\n\
 <script type=\"text/javascript\">\n\
      function initialize() {\n\
        var mapOptions = {\
          center: new google.maps.LatLng("+str(centern)+", "+str(centere)+"),\
          zoom: 12\
        };\n\
\n\
        var map = new google.maps.Map(document.getElementById(\"map-canvas\"), mapOptions);\n\
        var cctvIcon = \"cctv-camera-icon.png\"\n\
\n\
        var pathCoordinates = ["+pcoords+"];\n\
\n        // Chemin parcouru\n\
        var movePath = new google.maps.Polyline({\
            path: pathCoordinates, geodesic: true, strokeColor: '#FF0000', strokeOpacity: 1.0,strokeWeight: 2\
        });\n\
\n        // Cameras de surveillance\n\
        "+ccoords+"\n\
\n\
\n        // Locations\n\
        "+ecoords+"\n\
\n\
        movePath.setMap(map);\n\
      }\n\
      google.maps.event.addDomListener(window, 'load', initialize);\n\
    </script>\n"
    body="<div id=\"map-canvas\"></div>"
    return (js, body)
