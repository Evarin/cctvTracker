# Insertion dans la base de données
# Requêtes sur la base

from location import *

class CCTVDatabase:
    
    def __init__(self, sql=False):
        return

    def addCCTV(self, location):
        return

    def findCCTVs(self, location):
        return [location]

    @staticmethod
    def buildFromXML(file):
        db = CCTVDatabase()
        db.addFromXML(file)
        return db

    @staticmethod
    def buildFromSQL(file):
        db = CCTVDatabase()
        return db

def initDatabase():
    # Regarde si une base de données SQL a déjà été créée
    if True:
        db = CCTVDatabase.buildFromSQL("database.sql")
        return db
    # Sinon
    else:
        db = CCTVDatabase.buildFromXML("default.xml")
        return db
