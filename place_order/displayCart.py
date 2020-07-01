import uuid


def addToCart(mysql,qty,ProductID,Name,Description,Price,merchant_id,status,finalPrice,finalDiscountPrice,negotiatedRequestAmount):

    cur = mysql.connection.cursor()
    cur.execute('select NegotiationID from Negotiation ORDER BY NegotiationID ASC ')
    a = cur.fetchall()
    negotiation_id = uuid.uuid1()
    cart_id = uuid.uuid1()
    try:
        cur.execute("INSERT INTO Cart(CartID, Total,Status, MerchantID) VALUES('{}','{}','{}','{}')".format(cart_id,finalDiscountPrice,status,merchant_id))
        mysql.connection.commit()
    except Exception as e:
        print("Problem in inserting in db"+ str(e))
        return None
    loop = len(ProductID)
    for i in range(0,loop):
        try:
            cur.execute("INSERT INTO ProductCart(CartID, ProductID,Quantity) VALUES('{}','{}','{}')".format(cart_id,ProductID[i],qty[i]))
            mysql.connection.commit()
        except Exception as e:
            print("Problem in inseting into db"+str(e))
            return None

    if negotiatedRequestAmount!='0':
        try:
            cur.execute("INSERT INTO Negotiation(NegotiationID,Status,CartID,Price) VALUES('{}','{}','{}','{}')".format(negotiation_id,"pending",cart_id,negotiatedRequestAmount))
            mysql.connection.commit()
        except Exception as e:
            print("Problem in inserting in db"+ str(e))
            return None
    cur.close()


def getMerchantInfo(mysql,merchantID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT EmailID,ContactNumber FROM Merchant where MerchantID='{}'".format(merchantID))
    a = cur.fetchall()
    data = []
    data.append(a[0]['EmailID'])
    data.append(a[0]['ContactNumber'])
    return data