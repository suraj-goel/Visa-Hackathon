def displayOffersPage(mysql,merchantID):
    query = "select Offer.offerID as OfferID,Information,DiscountPercentage,ValidTill,QuantityRequired,Product.Name AS ProductName from Offer,OfferOnProduct,Product WHERE Offer.offerID = OfferOnProduct.OfferID AND OfferOnProduct.ProductID = Product.ProductID AND Product.MerchantID = '{}'".format(merchantID)
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = list(cur.fetchall())
    return data