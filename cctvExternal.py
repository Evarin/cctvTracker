# Recherche de données supplémentaires sur internet

import http.client

class ExternalRequester:
    googleAPIKey = "AIzaSyAQbUKKDk_G0y51l0BTiFP282hcbanlKs4"
	
    def __init__(self):
        return

    def findCCTVs(self, location):
        conn = http.client.HTTPSConnection("maps.googleapis.com")
        parametres = "key="+ExternalRequester.googleAPIKey+"&query=*+near&location="+str(location)+"&sensor=false"
        conn.request("GET", "/maps/api/place/nearbysearch/xml?"+parametres)
        print(conn.getresponse())
        return [location]

def initExternal():
    db = ExternalRequester()
    return db
