# Commons functions needed for the project

import math

googleAPIKey = "AIzaSyAQbUKKDk_G0y51l0BTiFP282hcbanlKs4"
# googleAPIKey = "AIzaSyChH08xskE0kNH_Ih9oO08wpK2LzYf9x5Y"


# Computes distance between two locations
def dist(loc1,loc2):
    degrees_to_radians = math.pi/180.0
    phi1 = (90.0 - loc1.north)*degrees_to_radians
    phi2 = (90.0 - loc2.north)*degrees_to_radians
    theta1 = loc1.east*degrees_to_radians
    theta2 = loc2.east*degrees_to_radians
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    # distance in km
    arc = arc * 6373
    return arc
