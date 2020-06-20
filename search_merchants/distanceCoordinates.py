import math
def distanceInKMBetweenCoordinates(lat1,long1,lat2,long2):
    earthRadiusKm = 6371
    dLat = math.radians(lat2-lat1)
    dLon = math.radians(long2-long1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return earthRadiusKm * c
