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

def getOffer(mysql,offerID):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM Offer WHERE offerID='{}'".format(offerID)
    cur.execute(query)
    offer = list(cur.fetchall())
    offer = offer[0]
    query = "SELECT Name FROM Product,OfferOnProduct WHERE Product.ProductID = OfferOnProduct.ProductID AND OfferOnProduct.OfferID = '{}'".format(offerID)
    cur.execute(query)
    product = list(cur.fetchall())
    offer['Products'] = product
    return offer

def updateoffersindb(mysql,merchantID,discount,info,date,quantity,productList,OfferID):
    cur = mysql.connection.cursor()
    query = "Update Offer SET Information = '{}' , DiscountPercentage='{}', ValidTill = '{}',QuantityRequired='{}' WHERE offerID = '{}'".format(info,discount,date,quantity,OfferID)
    cur.execute(query)
    mysql.connection.commit()
    cur.execute("DELETE FROM OfferOnProduct WHERE OfferID = '{}'".format(OfferID))
    mysql.connection.commit()
    # print(productList)
    for i in range(len(productList)):
        offerproductID = uuid.uuid1()
        query = "SELECT * FROM Product WHERE Name = '{}' AND MerchantID = '{}'".format(productList[i],merchantID)
        cur.execute(query)
        data = list(cur.fetchall())
        print(data[0]['ProductID'])
        print(offerproductID)
        query = "INSERT INTO OfferOnProduct VALUES('{}','{}','{}')".format(offerproductID,OfferID,data[0]['ProductID'])
        cur.execute(query)
        mysql.connection.commit()
    return "yes"