import uuid
def displayOffersPage(mysql,merchantID):
    query = "select DISTINCT Offer.offerID as OfferID,Information,DiscountPercentage,ValidTill,QuantityRequired  from Offer,OfferOnProduct,Product WHERE Offer.offerID = OfferOnProduct.OfferID AND OfferOnProduct.ProductID = Product.ProductID AND Product.MerchantID = '{}'".format(merchantID)
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = list(cur.fetchall())

    for i in range(len(data)):
        query = "SELECT Name,Description,Category FROM Product,OfferOnProduct WHERE OfferOnProduct.ProductID = Product.ProductID AND OfferOnProduct.OfferID='{}'".format(data[i]['OfferID'])
        cur.execute(query)
        products = cur.fetchall()
        if len(products)>0:
            data[i]['Products'] = products
        else:
            data[i]['Products'] = None

    return data

def addoffersindb(mysql,merchantID,discount,info,ValidTill,QuantityRequired,productList):
    cur = mysql.connection.cursor()
    offerID = uuid.uuid1()
    query = "INSERT INTO Offer VALUES('{}','{}','{}','{}','{}')".format(offerID,info,discount,ValidTill,QuantityRequired)
    cur.execute(query)
    mysql.connection.commit()

    for i in range(len(productList)):
        offerproductID = uuid.uuid1()
        query = "SELECT * FROM Product WHERE Name = '{}' AND MerchantID = '{}'".format(productList[i],merchantID)
        cur.execute(query)
        data = list(cur.fetchall())

        query = "INSERT INTO OfferOnProduct VALUES('{}','{}','{}')".format(offerproductID,offerID,data[0]['ProductID'])
        cur.execute(query)
        mysql.connection.commit()
    return "yes"