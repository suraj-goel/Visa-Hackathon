import uuid

def addToOrders(mysql,qty,ProductID,merchant_id,amount,currentDate,payment_flag='1',id=''):
    """
    :param mysql: database connection object
    :param qty: list of quantity of products purchased
    :param ProductID: list of unique products purchased
    :param merchant_id: buyer merchant unique identification number
    :param amount: total cost of product purchased
    :param currentDate: order date
    :param payment_flag: can take 3 values
    1 (default) is normal order
    2 is from order made from requirement
    3 is from order made from negotiation
    This is done to manage database according to the order made
    :param id: id is requirement id if payment_flag=2 or negotiation id if payment_flag=3
    """
    orderID = uuid.uuid1()
    cart_id = uuid.uuid1()
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO Cart(CartID, Total,Status, MerchantID) VALUES('{}','{}','{}','{}')".format(cart_id,amount,'P',merchant_id))
        mysql.connection.commit()
    except Exception as e:
        print("Problem in inserting cart in db"+ str(e))
        return None
    loop = len(ProductID)
    for i in range(0,loop):
        try:
            if int(qty[i])>0:
                cur.execute("INSERT INTO ProductCart(CartID, ProductID,Quantity) VALUES('{}','{}','{}')".format(cart_id,ProductID[i],qty[i]))
                mysql.connection.commit()
        except Exception as e:
            print("Problem in inserting products into db"+str(e))
            return None
    try:
        cur.execute("Insert INTO Orders(OrderID,CartID,OrderedDate) Values ('{}','{}','{}') ".format(orderID,cart_id,currentDate))
        mysql.connection.commit()
        if payment_flag == '2' and id != '':
            # requirement update
            cur.execute("update Requirement set Status='Done' where RequirementID='{}'".format(id))
            mysql.connection.commit()
        elif payment_flag == '3' and id != '':
            # negotiation update
            cur.execute("update Negotiation set Status='done' where NegotiationID='{}'".format(id))
            mysql.connection.commit()
    except Exception as e:
        print("Problem in updating orders or requirement or negotiation in db"+ str(e))
        return None
    cur.close()
    print("SUCCESSFUL PAYMENT")
