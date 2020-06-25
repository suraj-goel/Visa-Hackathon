import uuid


def addToOrders(mysql,qty,ProductID,Name,Description,Price,merchant_id,status,finalPrice,finalDiscountPrice,currentDate):

    orderID = uuid.uuid1()
    cart_id = uuid.uuid1()
    cur = mysql.connection.cursor()
    try:

        # print('INSERT INTO Cart(CartID, Total,Status, MerchantID) VALUES(%s,%s,%s,%s)',(cart_id,finalDiscountPrice,status,merchant_id))
        cur.execute('INSERT INTO Cart(CartID, Total,Status, MerchantID) VALUES(%s,%s,%s,%s)',(cart_id,finalDiscountPrice,'P',merchant_id))
        mysql.connection.commit()
    except Exception as e:
        print('*****')
        print("Problem in inserting in db"+ str(e))
        return None
    loop = len(ProductID)
    for i in range(0,loop):
        try:
            cur.execute('INSERT INTO ProductCart(CartID, ProductID,Quantity) VALUES(%s,%s,%s)',(cart_id,ProductID[i],qty[i]))
            mysql.connection.commit()
        except Exception as e:
            print('*****')
            print("Problem in inseting into db"+str(e))
            return None

    
        try:
            # print("Insert INTO Orders Values ('{}','no','{}','NULL','{}') ".format(orderID,cart_id,currentDate))
            cur.execute("Insert INTO Orders Values ('{}','no','{}','NULL','{}') ".format(orderID,cart_id,currentDate))
            mysql.connection.commit()
        except Exception as e:
            print('*****')
            print("Problem in inserting in db"+ str(e))
            return None
    cur.close()