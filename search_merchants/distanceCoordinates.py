import math
def distanceInKMBetweenCoordinates(lat1,long1,lat2,long2):
    earthRadiusKm =float(6371)
    dLat = math.radians(float(lat2)-float(lat1))
    dLon = math.radians(float(long2)-float(long1))
    lat1 = math.radians(float(lat1))
    lat2 = math.radians(float(lat2))
    a = float(math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2))
    c = float(2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
    return float(earthRadiusKm * c)
    
