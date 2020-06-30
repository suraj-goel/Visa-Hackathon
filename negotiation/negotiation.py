import numpy as np
#buyer
def displayAllNegotiation(mysql,merchant_id):
    cur = mysql.connection.cursor()

    negotiationCollection = []
    productCartList = []
    contactInfo = []
    cur.execute("select * from Negotiation,Cart where Cart.CartID=Negotiation.CartID and Cart.Status = 'N' and Cart.MerchantID='{}'".format(merchant_id))
    a = cur.fetchall()
    for i in a:
        if (i['Status'] == 'done'):
            continue
        else:
            negotiationCollection.append(i)
            cur.execute("select distinct * from Negotiation,Cart,ProductCart,Product where Negotiation.CartID=Cart.CartID and Cart.CartID=ProductCart.CartID and Negotiation.NegotiationID='{}' and Product.ProductID=ProductCart.ProductID".format(i['NegotiationID']))
            b = cur.fetchall()
            productCartList.append(b)
            cur.execute("select * from Merchant where MerchantID='{}'".format(b[0]['Product.MerchantID']))
            c = cur.fetchall()
            contactInfo.append(c)
    print(productCartList)

    return [negotiationCollection,productCartList,contactInfo]

#buyer
def displayNegotiationType(mysql,merchant_id,status):
    cur = mysql.connection.cursor()
    if(status == 'A'):
        status = 'accepted'
    elif(status == 'D'):
        status = 'rejected'
    elif(status == 'R'):
        status = 'pending'
    cur = mysql.connection.cursor()

    negotiationCollection = []
    productCartList = []
    contactInfo = []
    cur.execute("select * from Negotiation,Cart where Cart.CartID=Negotiation.CartID and Cart.Status='{}'and Cart.MerchantID='{}' and Negotiation.Status='{}'".format('N',merchant_id,status))
    a = cur.fetchall()
    print(status)

    for i in a:
        negotiationCollection.append(i)
        cur.execute("select distinct * from Negotiation,Cart,ProductCart,Product where Negotiation.CartID=Cart.CartID and Cart.CartID=ProductCart.CartID and Negotiation.NegotiationID='{}' and Product.ProductID=ProductCart.ProductID".format(i['NegotiationID']))
        b = cur.fetchall()
        productCartList.append(b)
        cur.execute("select * from Merchant where MerchantID='{}'".format(b[0]['Product.MerchantID']))
        c = cur.fetchall()
        contactInfo.append(c)
    print(productCartList)
    print(contactInfo)
    return [negotiationCollection,productCartList,contactInfo]
#buyer
def deleteNegotiation(mysql,negotiationID):
    cur = mysql.connection.cursor()
    cur.execute("delete from Negotiation where NegotiationID='{}'".format(negotiationID))
    mysql.connection.commit()
#supplier
def showNegotiation(mysql,merchant_id):
    cur = mysql.connection.cursor()
    cur.execute("select ProductID from Product where MerchantID='{}'".format(merchant_id))
    a = cur.fetchall()
    CartList= []
    for i in a:
        cur.execute("select CartID from ProductCart where ProductID='{}'".format(i['ProductID']))
        b = cur.fetchall()
        for j in b:
            CartList.append(j)

    uniCart = list(set(val for dic in CartList for val in dic.values()))

    NegList = []
    for i in uniCart:
        cur.execute("select NegotiationID from Negotiation where CartID='{}' and Negotiation.Status='pending'".format(i))
        b = cur.fetchall()
        for j in b:
            NegList.append(j)
    uniNeg = list(set(val for dic in NegList for val in dic.values()))
    contactInfo = []
    productCartList = []
    Amount = []
    for i in uniNeg:
        cur.execute("select distinct * from Negotiation,Cart,ProductCart,Product where Negotiation.CartID=Cart.CartID and Cart.CartID=ProductCart.CartID and Negotiation.NegotiationID='{}' and Product.ProductID=ProductCart.ProductID and Negotiation.Status='pending'".format(i))
        b = cur.fetchall()
        productCartList.append(b)
        cur.execute("select * from Negotiation,Cart where Negotiation.NegotiationID='{}' and Negotiation.CartID=Cart.CartID".format(i))
        Amount.append(cur.fetchall())
        cur.execute("select Merchant.RegisteredName,Merchant.MerchantID,Merchant.Name,Merchant.ContactNumber, Merchant.EmailID from Cart,Negotiation,Merchant where Cart.CartID = Negotiation.CartID and Cart.MerchantID=Merchant.MerchantID and Negotiation.NegotiationID='{}'".format(i))
        contactInfo.append(cur.fetchall())

    print(productCartList)
    print(contactInfo)
    print(Amount)
    return [contactInfo,productCartList,Amount]


#supplier
def updateNegotiation(mysql,negotiationID,status,NegAmount):
    cur = mysql.connection.cursor()
    print(negotiationID)
    status = str(status)
    cur.execute("UPDATE Negotiation SET Status = '{}',Price = '{}' where NegotiationID = '{}' ".format(status, NegAmount, negotiationID))
    mysql.connection.commit()
    cur.execute("select NegotiationID from Negotiation where NegotiationID = '{}'".format(negotiationID))
    print(cur.fetchall())
    return "Success"

