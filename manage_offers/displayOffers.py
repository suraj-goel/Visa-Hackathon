def displayOffersPage(mysql,merchantID):
    query = "select Offer.offerID as OfferID,Information,DiscountPercentage,ValidTill,QuantityRequired  from Offer,OfferOnProduct,Product WHERE Offer.offerID = OfferOnProduct.OfferID AND OfferOnProduct.ProductID = Product.ProductID AND Product.MerchantID = '{}'".format(merchantID)
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