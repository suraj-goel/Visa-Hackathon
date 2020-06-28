import uuid


def addToOrders(mysql,qty,ProductID,merchant_id,amount,currentDate,requirement_flag=False,requirementid=''):
    orderID = uuid.uuid1()
    cart_id = uuid.uuid1()
    cur = mysql.connection.cursor()

    try:
        # print('INSERT INTO Cart(CartID, Total,Status, MerchantID) VALUES(%s,%s,%s,%s)',(cart_id,finalDiscountPrice,status,merchant_id))
        print(cart_id,amount,'P',merchant_id)
        cur.execute("INSERT INTO Cart(CartID, Total,Status, MerchantID) VALUES(%s,%s,%s,%s)",(cart_id,amount,'P',merchant_id))
        mysql.connection.commit()
        print("Added to Cart Table")

    except Exception as e:
        print('*****')
        print("Problem in inserting in db"+ str(e))
        return None

    loop = len(ProductID)
    for i in range(0,loop):
        try:
            if int(qty[i])>0:
                cur.execute('INSERT INTO ProductCart(CartID, ProductID,Quantity) VALUES(%s,%s,%s)',(cart_id,ProductID[i],qty[i]))
                mysql.connection.commit()
        except Exception as e:
            print('*****')
            print("Problem in inseting into db"+str(e))
            return None
    try:
        # print("Insert INTO Orders Values ('{}','no','{}','NULL','{}') ".format(orderID,cart_id,currentDate))
        cur.execute("Insert INTO Orders(OrderID,CartID,OrderedDate) Values ('{}','{}','{}') ".format(orderID,cart_id,currentDate))
        mysql.connection.commit()
        print("Added to Orders table")
        if requirement_flag==True and requirementid!='':
            cur.execute("update Requirement set Status='Done' where RequirementID=%s;",(requirementid))
            mysql.connection.commit()
            print('completed requirement')
    except Exception as e:
        print('*****')
        print("Problem in inserting in db"+ str(e))
        return None
    cur.close()
