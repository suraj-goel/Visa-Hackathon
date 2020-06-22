def displayAllProducts(mysql,selectedMerchant):
    cur = mysql.connection.cursor()
    cur.execute("select ProductID, Name, Description, Price, Quantity, Category FROM Product WHERE MerchantID = " + str(selectedMerchant))
    a=cur.fetchall()
    
    currentProductID = str(a[0]["ProductID"])
    currentName = str(a[0]["Name"])
    currentDescription = str(a[0]["Description"])
    currentPrice = str(a[0]["Price"])
    currentQuantity = str(a[0]["Quantity"])
    currentCategory = str(a[0]["Category"])

    # print("\n1st row ->", currentProductID, currentName, currentDescription, currentPrice, currentQuantity, currentCategory, "\n")
    cur.close()
    
    productList = []
    
    for i in range(len(a)):
        currentProductID = str(a[i]["ProductID"])
        currentName = str(a[i]["Name"])
        currentDescription = str(a[i]["Description"])
        currentPrice = str(a[i]["Price"])
        currentQuantity = str(a[i]["Quantity"])
        currentCategory = str(a[i]["Category"])
        temp = {"ProductID": currentProductID,
                "Name": currentName,
                "Description": currentDescription,
                "Price": currentPrice,
                "Quantity": currentQuantity,
                "Category": currentCategory
        }
        productList.append(temp)
    
    return productList

def displayAllOffers(mysql, selectedMerchant):
    cur = mysql.connection.cursor()
    cur.execute("select ProductID from Product WHERE MerchantID = " + str(selectedMerchant))
    a=cur.fetchall()
    # cur.close()

    offers = {}

    for i in range(len(a)):
        cur.execute("select Information,OfferOnProduct.OfferID as OfferID, Offer.DiscountPercentage as DiscountPercentage \
        , Offer.QuantityRequired as QuantityRequired \
        from OfferOnProduct, Offer WHERE ProductID = " + str(a[i]['ProductID']) + " \
        and OfferOnProduct.OfferID = Offer.OfferID")
        offerProduct = cur.fetchall()

        if len(offerProduct) > 0:
            offers[a[i]['ProductID']] = offerProduct
        else:
            offers[a[i]['ProductID']] = ()
    
    print(offers)
    return offers
