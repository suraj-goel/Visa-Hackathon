def getAllProducts(mysql,merchantID,filter='A'):
    """
    :param mysql: database connection object
    :param merchantID: unique merchant identifier
    :param filter: user filter to view S(Selling products), N(Not selling products) and A(All products)
    :return: returns a list of products based on filter
    """
    cur = mysql.connection.cursor()
    if filter=='S':
        query='select * from Product where Sell=1 and MerchantID='+str(merchantID)+';'
    if filter=='N':
        query='select * from Product where Sell=0 and MerchantID='+str(merchantID)+';'
    if filter=='A':
        query = 'select * from Product where MerchantID='+str(merchantID)+';'
    cur.execute(query)
    product_list=list(cur.fetchall())
    for i in range(len(product_list)):
            cur.execute("select Information,OfferOnProduct.OfferID as OfferID, Offer.DiscountPercentage as DiscountPercentage \
            , Offer.QuantityRequired as QuantityRequired \
            from OfferOnProduct, Offer WHERE ProductID = " + "'" + str(product_list[i]['ProductID']) + "' \
            and OfferOnProduct.OfferID = Offer.OfferID")
            offerProduct = cur.fetchall()
            if len(offerProduct) > 0:
                product_list[i]['offers']= offerProduct
            else:
                product_list[i]['offers']= None
    cur.close()
    return product_list