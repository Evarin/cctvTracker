googleAPIKey = "AIzaSyAQbUKKDk_G0y51l0BTiFP282hcbanlKs4"

def exportHTML(path, cctv):
    pcoords = ""
    centern = 0.
    centere = 0.
    for loc in path:
        pcoords += "new google.maps.LatLng("+str(loc.north)+", "+str(loc.east)+"),\n"
        centern += loc.north
        centere += loc.east
    ccoords = ""
    cctvsCoord=set([(loc.north, loc.east) for loc in cctv])
    for (n,e) in cctvsCoord:
        ccoords += "new google.maps.Marker({ position: new google.maps.LatLng("+str(n)+", "+str(e)+"),\
 map: map, title: 'Camera'});\n";
    pcoords=pcoords[:-2]
    centern/=len(path)
    centere/=len(path)
    output = "<html>\n<head>\n <title>Smile, you're on TV</title>\n <meta name=\"viewport\" content=\"initial-scale=1.0, user-scalable=yes\" />\n\
 <style type=\"text/css\">\n html { height: 100% }\n body { height: 100%; margin: 0; padding: 0 }\n #map-canvas { height: 100% }\n </style>\n\
 <script type=\"text/javascript\" src=\"https://maps.googleapis.com/maps/api/js?key="+googleAPIKey+"&sensor=false\"></script>\n\
 <script type=\"text/javascript\">\n\
      function initialize() {\n\
        var mapOptions = {\
          center: new google.maps.LatLng("+str(centern)+", "+str(centere)+"),\
          zoom: 12\
        };\n\
\n\
        var map = new google.maps.Map(document.getElementById(\"map-canvas\"), mapOptions);\n\
\n\
        var pathCoordinates = ["+pcoords+"];\n\
\n        // Chemin parcouru\n\
        var movePath = new google.maps.Polyline({\
            path: pathCoordinates, geodesic: true, strokeColor: '#FF0000', strokeOpacity: 1.0,strokeWeight: 2\
        });\n\
\n        // Caméras de surveillance\n\
        "+ccoords+"\n\
\n\
        movePath.setMap(map);\n\
      }\n\
      google.maps.event.addDomListener(window, 'load', initialize);\n\
    </script>\n\
  </head>\n\
  <body>\
    <div id=\"map-canvas\"/>\
  </body>\n\
</html>"
    return output
