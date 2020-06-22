def displayALLCart(mysql,cartID,merchantID):
    cur = mysql.connection.cursor()
    cur.execute("select * FROM ProductCart WHERE CartID = "+str(cartID))
    results=cur.fetchall()


    cur.close()

    cartList = []

    for i in range(len(results)):
        currentProductID = str(results[i]["ProductID"])
        currentMerchantID = str(results[i]["MerchantID"])
        currentPrice = str(results[i]["Price"])
        currentStatus = str(results[i]["Status"])
        currentQuantity = str(results[i]["Quantity"])
        currentInformation = str(results[i]["Information"])
        if(currentStatus=='pending'):
                temp = {"ProductID": currentProductID,
                "Description": currentInformation,
                "Price": currentPrice,
                "Quantity": currentQuantity,
                }
                cartList.append(temp)


    return cartList
