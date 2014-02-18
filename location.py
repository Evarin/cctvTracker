# Structure de données et extraction des coordonnées GPS / KML

class Location:
    
    def __init__(self, north=0, east=0.):
        self.north=north
        self.east=east

    def __repr__(self):
        return str(self.north) + "N, " + str(self.east) + "E"
