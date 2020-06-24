def getAllProducts(mysql,merchantID,filter='A'):
    cur = mysql.connection.cursor()
    if filter=='S':
        query='select * from Product where Sell=1 and MerchantID='+str(merchantID)+';'
    if filter=='N':
        query = query='select * from Product where Sell=0 and MerchantID='+str(merchantID)+';'
    if filter=='A':
        query = 'select * from Product where MerchantID='+str(merchantID)+';'
    cur.execute(query)
    a=list(cur.fetchall())
    for i in range(len(a)):
            cur.execute("select Information,OfferOnProduct.OfferID as OfferID, Offer.DiscountPercentage as DiscountPercentage \
            , Offer.QuantityRequired as QuantityRequired \
            from OfferOnProduct, Offer WHERE ProductID = " + "'" + str(a[i]['ProductID']) + "' \
            and OfferOnProduct.OfferID = Offer.OfferID")
            offerProduct = cur.fetchall()
            if len(offerProduct) > 0:
                a[i]['offers']= offerProduct
            else:
                a[i]['offers']= None
    return a