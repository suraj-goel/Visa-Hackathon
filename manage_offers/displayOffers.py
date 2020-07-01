import uuid


def displayOffersPage(mysql, merchantID):
    """
    :param mysql: database connection object
    :param merchantID: unique merchant identifier
    :return: returns all products along with offer information
    """
    query = "select DISTINCT Offer.offerID as OfferID,Information,DiscountPercentage,ValidTill,QuantityRequired " \
            " from Offer,OfferOnProduct,Product WHERE Offer.offerID = OfferOnProduct.OfferID AND OfferOnProduct." \
            "ProductID = Product.ProductID AND Product.MerchantID = '{}'".format(merchantID)
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = list(cur.fetchall())
    for i in range(len(data)):
        query = "SELECT Name,Description,Category FROM Product,OfferOnProduct WHERE OfferOnProduct.ProductID = " \
                "Product.ProductID AND OfferOnProduct.OfferID='{}'".format(data[i]['OfferID'])
        cur.execute(query)
        products = cur.fetchall()
        if len(products) > 0:
            data[i]['Products'] = products
        else:
            data[i]['Products'] = None
    cur.close()
    return data


def addoffersindb(mysql, merchantID, discount, info, ValidTill, QuantityRequired, productList):
    """
    :param mysql: database connection object
    :param merchantID: unique merchant identifier
    :param discount: discount percentage
    :param info: information about offer to be displayed to others
    :param ValidTill: validity date
    :param QuantityRequired: amount of products to be purchased for offer to be applicable
    :param productList: list of products to which this offer can be applied
    :return: adds offer to database and returns "yes" on success
    """
    cur = mysql.connection.cursor()
    offerID = uuid.uuid1()
    query = "INSERT INTO Offer VALUES('{}','{}','{}','{}','{}')".format(offerID, info, discount, ValidTill,QuantityRequired)
    cur.execute(query)
    mysql.connection.commit()
    for i in range(len(productList)):
        offerproductID = uuid.uuid1()
        query = "SELECT * FROM Product WHERE Name = '{}' AND MerchantID = '{}'".format(productList[i], merchantID)
        cur.execute(query)
        data = list(cur.fetchall())
        query = "INSERT INTO OfferOnProduct VALUES('{}','{}','{}')".format(offerproductID, offerID, data[0]['ProductID'])
        cur.execute(query)
        mysql.connection.commit()
    return "yes"


def getOffer(mysql, offerID):
    """
    :param mysql: database connection object
    :param offerID: unique offer identifier
    :return: offer details and list of products which associate with the offer
    """
    cur = mysql.connection.cursor()
    query = "SELECT * FROM Offer WHERE offerID='{}'".format(offerID)
    cur.execute(query)
    offer = list(cur.fetchall())
    offer = offer[0]
    query = "SELECT Name FROM Product,OfferOnProduct WHERE Product.ProductID = OfferOnProduct.ProductID AND " \
            "OfferOnProduct.OfferID = '{}'".format(offerID)
    cur.execute(query)
    product = list(cur.fetchall())
    offer['Products'] = product
    return offer


def updateoffersindb(mysql, merchantID, discount, info, date, quantity, productList, OfferID):
    """
    :param mysql: database connection object
    :param merchantID: unique merchant identifier
    :param discount: updated discount
    :param info: updated offer information
    :param date: updated validity date
    :param quantity: updated quantity
    :param productList: updated list of products to which offer is applicable
    :param OfferID: unique offer identifier
    :return: updated offer information in database and returns "yes" if successful
    """
    cur = mysql.connection.cursor()
    query = "Update Offer SET Information = '{}' , DiscountPercentage='{}', ValidTill = '{}',QuantityRequired='{}' " \
            "WHERE offerID = '{}'".format(info, discount, date, quantity, OfferID)
    cur.execute(query)
    mysql.connection.commit()
    cur.execute("DELETE FROM OfferOnProduct WHERE OfferID = '{}'".format(OfferID))
    mysql.connection.commit()
    for i in range(len(productList)):
        offerproductID = uuid.uuid1()
        query = "SELECT * FROM Product WHERE Name = '{}' AND MerchantID = '{}'".format(productList[i], merchantID)
        cur.execute(query)
        data = list(cur.fetchall())
        query = "INSERT INTO OfferOnProduct VALUES('{}','{}','{}')".format(offerproductID, OfferID,data[0]['ProductID'])
        cur.execute(query)
        mysql.connection.commit()
    return "yes"
