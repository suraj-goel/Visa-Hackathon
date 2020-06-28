#buyer
def displayAllNegotiation(mysql,merchant_id):
    cur = mysql.connection.cursor()

    negotiationCollection = []
    productCartList = []
    cur.execute("select * from Negotiation,Cart where Cart.CartID=Negotiation.CartID and Cart.Status = 'N' and Cart.MerchantID='{}'".format(merchant_id))
    a = cur.fetchall()
    for i in a:
        if (i['Status'] == 'done'):
            continue
        else:
            negotiationCollection.append(i)
            cur.execute("select Product.Name,ProductCart.Quantity from Product,ProductCart where ProductCart.CartID='{}' and Product.ProductID=ProductCart.ProductID".format(i['CartID']))
            productCartList.append(cur.fetchall())
    print(negotiationCollection,productCartList)

    return [negotiationCollection,productCartList]

#buyer
def displayNegotiationType(mysql,merchant_id,status):
    cur = mysql.connection.cursor()
    if(status == 'A'):
        status = 'accept'
    elif(status == 'D'):
        status = 'reject'
    elif(status == 'R'):
        status = 'pending'
    cur = mysql.connection.cursor()

    negotiationCollection = []
    productCartList = []
    cur.execute("select * from Negotiation,Cart where Cart.CartID=Negotiation.CartID and Cart.Status='{}'and Cart.MerchantID='{}' and Negotiation.Status='{}'".format('N',merchant_id,status))
    a = cur.fetchall()
    print(status)

    for i in a:
        negotiationCollection.append(i)
        cur.execute("select Product.Name,ProductCart.Quantity from Product,ProductCart where ProductCart.CartID='{}' and Product.ProductID=ProductCart.ProductID".format(i['CartID']))
        productCartList.append(cur.fetchall())
    print(negotiationCollection,productCartList)
    return [negotiationCollection,productCartList]
#buyer
def deleteNegotiation(mysql,negotiationID):
    cur = mysql.connection.cursor()
    cur.execute("delete from Negotiation where Status='pending' and NegotiationID='{}'".format(negotiationID))
    mysql.connection.commit()
#supplier
def showNegotiation(mysql,merchant_id):
    cur = mysql.connection.cursor()
    cur.execute("select Cart.CartID from Negotiation,Cart where Negotiation.Status='pending' and Negotiation.CartID=Cart.CartID and Cart.Status='N'")
    a = cur.fetchall()
    purchaseCart = []
    totalAmountCart = []
    for i in a:
        cur.execute("select ProductID from ProductCart where CartID='{}'".format(i['CartID']))
        oneItem = cur.fetchall()[0]
        cur.execute("select MerchantID from Product where ProductID='{}'".format(oneItem['ProductID']))
        merchantID = cur.fetchall()[0]
        #print(merchantID)
        if(merchantID['MerchantID'] == merchant_id):

            cur.execute("select Product.Name,ProductCart.Quantity from ProductCart,Product where CartID='{}' ".format(i['CartID']))
            b=cur.fetchall()
            purchaseCart.append(b)
            cur.execute("select Negotiation.NegotiationID,Cart.Total,Negotiation.Price from Cart,Negotiation where Cart.CartID=Negotiation.CartID and Negotiation.CartID='{}'".format(i['CartID']))
            c = cur.fetchall()
            totalAmountCart.append(c)
    print("show")
    print(purchaseCart,totalAmountCart)
    return [purchaseCart,totalAmountCart]

#suppier
def confirmNegotiation(mysql,negotiationID):
    cur = mysql.connection.cursor()
    cur.execute("Update Negotiation SET Status = 'accept' WHERE NegotiationID = '{}' ".format(negotiationID))
    mysql.connection.commit()
    return "Success"

def rejectNegotiation(mysql,negotiationID):
    cur = mysql.connection.cursor()
    cur.execute("Update Negotiation SET Status = 'reject' WHERE NegotiationID = '{}' ".format(negotiationID))
    mysql.connection.commit()
    return "Success"

