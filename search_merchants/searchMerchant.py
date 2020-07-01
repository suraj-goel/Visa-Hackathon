from orders_management.orderHistory import SearchRatings
from .distanceCoordinates import distanceInKMBetweenCoordinates


def getCurrentLocation(mysql, merchantID):
    """
    :param mysql: database connection object
    :param merchantID: unique merchant identification number
    :return: location of merchant
    """
    cur = mysql.connection.cursor()
    cur.execute("select Latitude,Longitude FROM Location WHERE MerchantID = " + str(merchantID))
    a = cur.fetchall()
    cur.close()
    return a[0]


def getAllMerchants(mysql, merchantID, radius):
    """
    :param mysql: database connection object
    :param merchantID: unique merchant identification number
    :param radius: search radius in km
    :return: list of merchants with discount information based on search radius
    """
    cur = mysql.connection.cursor()
    cur.execute("select Latitude,Longitude FROM Location WHERE MerchantID = " + str(merchantID))
    a = cur.fetchall()
    currentLatitude = float(a[0]["Latitude"])
    currentLongitude = float(a[0]["Longitude"])
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute(
        "select LocationID,Latitude,Longitude,Merchant.MerchantID,Name,RegisteredName,EmailID,ContactNumber from "
        "Location INNER JOIN Merchant ON Location.MerchantID =Merchant.MerchantID WHERE Merchant.MerchantID!=" +
        "'" + str(merchantID) + "'" + ";")
    a = cur.fetchall()
    nearbymerchants = []
    for i in range(len(a)):
        latitude = float(a[i]["Latitude"])
        longitude = float(a[i]["Longitude"])
        distance = distanceInKMBetweenCoordinates(currentLatitude, currentLongitude, latitude, longitude)
        if distance <= radius:
            dic = {"distance": distance}
            dic.update(a[i])
            nearbymerchants.append(dic)
    data_res = []
    for i in nearbymerchants:
        cur.execute("select distinct * from Product,Offer,OfferOnProduct where Product.MerchantID=%s and "
                    "Product.ProductID = OfferOnProduct.ProductID and OfferOnProduct.offerID = Offer.offerID "
                    "and CURDATE()<=ValidTill and Product.Sell=1", (i['MerchantID'],))
        x = list(cur.fetchall())
        if x:
            i['Offers'] = x
        i['rate'] = SearchRatings(mysql, i['MerchantID'])
        data_res.append(i)
    cur.close()
    return data_res
