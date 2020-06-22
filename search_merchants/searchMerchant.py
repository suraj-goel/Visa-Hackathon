
from .distanceCoordinates import distanceInKMBetweenCoordinates
def getAllMerchants(mysql,merchantID,radius=2000):
    cur = mysql.connection.cursor()
    cur.execute("select Latitude,Longitude FROM Location WHERE MerchantID = " + str(merchantID))
    a=cur.fetchall()
    currentLatitude = float(a[0]["Latitude"])
    
    currentLongitude = float(a[0]["Longitude"])
    cur.close()

    
    cur = mysql.connection.cursor()
    cur.execute("select LocationID,Latitude,Longitude,Merchant.MerchantID,Name,RegisteredName,EmailID,ContactNumber from Location INNER JOIN Merchant ON Location.MerchantID =Merchant.MerchantID WHERE Merchant.MerchantID!="+"'"+str(merchantID)+"'"+";")

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
    data_res = []

    for i in nearbymerchants:
            cur.execute("select distinct * from Product,Offer,OfferOnProduct where Product.MerchantID=%s and Product.ProductID = OfferOnProduct.ProductID and OfferOnProduct.offerID = Offer.offerID and CURDATE()<=ValidTill", (i['MerchantID'],))
            x = list(cur.fetchall())
            i['Offers'] = x
            data_res.append(i)

    cur.close()
    finalResult = []
    for i in range(len(data_res)):
        latitude = float(data_res[i]["Latitude"])
        longitude = float(data_res[i]["Longitude"])
        distance = distanceInKMBetweenCoordinates(currentLatitude,currentLongitude,latitude,longitude)
        dic = {"distance" : distance}
        dic.update(data_res[i])
        if not radius:
            finalResult.append(dic)
        else:
            if (distance<=float(radius)): 
                finalResult.append(dic)
    finalResult = sorted(finalResult, key = lambda i: i['distance'])
    # print(finalResult)
    return finalResult

def getCurrentLocation(mysql,merchantID):
    cur = mysql.connection.cursor()
    cur.execute("select Latitude,Longitude FROM Location WHERE MerchantID = " + str(merchantID))
    a=cur.fetchall()
    cur.close()
    return a[0]





    