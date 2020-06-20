from builtins import list, len


def getSearchResults(mysql,name,merchantid,search_option,filters):
    cur = mysql.connection.cursor()
    print(filters)
    if search_option=='product':
        product=name
        # only offers filter
        if filters:
            cur.execute("SELECT * from Product,Offer,OfferOnProduct WHERE (NAME like %s OR Category like %s ) and MerchantID <> %s and Product.ProductID = OfferOnProduct.ProductID and OfferOnProduct.offerID = Offer.offerID and CURDATE()<=ValidTill",
                        ("%" + product + "%", "%" + product + "%", merchantid))
            data = list(cur.fetchall())

            # similar category search
            product_tags = product.split(" ")
            if len(product_tags) > 1:
                for i in product_tags:
                    cur.execute("SELECT * from Merchant,Product,Offer,OfferOnProduct WHERE Category LIKE %s and MerchantID <> %s and Product.ProductID = OfferOnProduct.ProductID and OfferOnProduct.offerID = Offer.offerID and CURDATE()<=ValidTill", (i, merchantid))
                    x = list(cur.fetchall())
                    data.extend(x)
            return data
        else:
            # add exact matches then based on name then see similarity in name
            cur.execute("SELECT * from Merchant,Product WHERE (Product.Name like %s OR Category like %s ) and Product.MerchantID <> %s and Product.MerchantID=Merchant.MerchantID",
                    ("%"+product+"%","%"+product+"%",merchantid))
            data = list(cur.fetchall())

            # similar category search
            product_tags=product.split(" ")
            if len(product_tags)>1:
                for i in product_tags:
                    cur.execute("SELECT * from Merchant,Product WHERE Category LIKE %s and Product.MerchantID <> %s", ( i,merchantid))
                    x=list(cur.fetchall())
                    data.extend(x)

            # make search unique and append discount info only valid ones
            res=[]
            data_res=[]
            for i in data:
                if i['ProductID'] not in res:
                    cur.execute("select distinct * from Offer,OfferOnProduct where OfferOnProduct.ProductID=%s and OfferOnProduct.offerID = Offer.offerID and CURDATE()<=ValidTill", (i['ProductID'],))
                    x=list(cur.fetchall())
                    i['Offers']=x
                    res.append(i['ProductID'])
                    data_res.append(i)
            print(data_res)
            return data_res
    else:
        merchant=name
        if filters:
            cur.execute("SELECT * from Merchant,Product,Offer,OfferOnProduct WHERE Merchant.Name LIKE %s and MerchantID <> %s and Product.ProductID = OfferOnProduct.ProductID and OfferOnProduct.offerID = Offer.offerID and CURDATE()<=ValidTill", ("%"+merchant+"%", merchantid))
            data = list(cur.fetchall())
            return data
        else:
            # add exact matches then based on name then see similarity in name
            cur.execute("SELECT * from Merchant,Product WHERE Merchant.Name like %s and Product.MerchantID <> %s and Product.MerchantID=Merchant.MerchantID",
                    ("%"+merchant+"%",merchantid))
            data = list(cur.fetchall())


