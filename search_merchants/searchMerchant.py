
from .distanceCoordinates import distanceInKMBetweenCoordinates
def getAllMerchants(mysql,merchantID,radius):
    cur = mysql.connection.cursor()
    cur.execute("select Latitude,Longitude FROM Location WHERE MerchantID = " + str(merchantID))
    a=cur.fetchall()
    currentLatitude = float(a[0]["Latitude"])
    
    currentLongitude = float(a[0]["Longitude"])
    cur.close()

    
    cur = mysql.connection.cursor()
    cur.execute("select LocationID,Latitude,Longitude,Merchant.MerchantID,Name,RegisteredName,EmailID,ContactNumber from Location INNER JOIN Merchant ON Location.MerchantID =Merchant.MerchantID;")
    a=cur.fetchall()

    nearbymerchants = []
    for i in range(len(a)):
        latitude = float(a[i]["Latitude"])
        longitude = float(a[i]["Longitude"])
        distance = distanceInKMBetweenCoordinates(currentLatitude,currentLongitude,latitude,longitude)
        if distance <= radius:
            dic = {"distance" : distance}
            dic.update(a[i])
            nearbymerchants.append(dic)

    cur.close()
    return nearbymerchants

def getCurrentLocation(mysql,merchantID):
    cur = mysql.connection.cursor()
    cur.execute("select Latitude,Longitude FROM Location WHERE MerchantID = " + str(merchantID))
    a=cur.fetchall()
    cur.close()
    return a[0]





    