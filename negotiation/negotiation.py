# buyer profile
def displayAllNegotiation(mysql,merchant_id):
    """
    :param mysql: database connection object
    :param merchant_id: unique merchant identification number
    :return: list of requested negotiations, products under the negotiation cart and supplier merchant information
    """
    cur = mysql.connection.cursor()
    negotiationCollection = []
    productCartList = []
    contactInfo = []
    cur.execute("select * from Negotiation,Cart where Cart.CartID=Negotiation.CartID and Cart.Status = 'N' and "
                "Cart.MerchantID='{}'".format(merchant_id))
    negotiations = cur.fetchall()
    for i in negotiations:
        if (i['Status'] == 'done'):
            continue
        else:
            negotiationCollection.append(i)
            cur.execute("select distinct * from Negotiation,Cart,ProductCart,Product where Negotiation.CartID=Cart.CartID "
                        "and Cart.CartID=ProductCart.CartID and Negotiation.NegotiationID='{}' and Product.ProductID="
                        "ProductCart.ProductID".format(i['NegotiationID']))
            products = cur.fetchall()
            productCartList.append(products)
            cur.execute("select * from Merchant where MerchantID='{}'".format(products[0]['Product.MerchantID']))
            merchants_info = cur.fetchall()
            contactInfo.append(merchants_info)
    return [negotiationCollection,productCartList,contactInfo]

def displayNegotiationType(mysql,merchant_id,status):
    """
    :param mysql: database connection object
    :param merchant_id: unique merchant identification number
    :param status: status of negotiation can be A(Accepted), D(Rejected), R(Pending)
    :return: list of requested negotiations, products under the negotiation cart and supplier merchant information
    based on status
    """
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
    cur.execute("select * from Negotiation,Cart where Cart.CartID=Negotiation.CartID and Cart.Status='{}'and Cart."
                "MerchantID='{}' and Negotiation.Status='{}'".format('N',merchant_id,status))
    negotiation = cur.fetchall()
    for i in negotiation:
        negotiationCollection.append(i)
        cur.execute("select distinct * from Negotiation,Cart,ProductCart,Product where Negotiation.CartID=Cart.CartID "
                    "and Cart.CartID=ProductCart.CartID and Negotiation.NegotiationID='{}' and Product.ProductID="
                    "ProductCart.ProductID".format(i['NegotiationID']))
        products = cur.fetchall()
        productCartList.append(products)
        cur.execute("select * from Merchant where MerchantID='{}'".format(products[0]['Product.MerchantID']))
        merchants_info = cur.fetchall()
        contactInfo.append(merchants_info)
    cur.close()
    return [negotiationCollection,productCartList,contactInfo]


def deleteNegotiation(mysql,negotiationID):
    """
    :param mysql: database connection object
    :param negotiationID: unique negotiation identification number
    deletes a negotiation request
    """
    cur = mysql.connection.cursor()
    cur.execute("delete from Negotiation where NegotiationID='{}'".format(negotiationID))
    mysql.connection.commit()


# supplier profile
def showNegotiation(mysql,merchant_id):
    """
    :param mysql: database connection object
    :param merchant_id: unique merchant identification number
    :return: list of received negotiations and contact information of buyer merchant
    """
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
    cur.close()
    return [contactInfo,productCartList,Amount]


def updateNegotiation(mysql,negotiationID,status,NegAmount):
    """
    :param mysql: database connection object
    :param negotiationID: unique negotiation identification number
    :param status: status of negotiation can be accepted or rejected by supplier
    :param NegAmount: updated negotiation amount if supplier accepts
    :return:
    """
    cur = mysql.connection.cursor()
    cur.execute("Update Negotiation SET Status = '{}' , Price = '{}' WHERE NegotiationID = '{}';".format(status,NegAmount,negotiationID))
    mysql.connection.commit()
    return "Success"

