
def addToCart(mysql,qty,ProductID,Name,Description,Price,merchant_id,status):

    cur = mysql.connection.cursor()
    cur.execute("select CartID FROM ProductCart where MerchantID =%s ORDER BY CartID",(str(merchant_id)))
    a=cur.fetchall()
    cart_id = 1
    for i in range(0,len(a)):
        if str(a[i]['CartID']) != str(cart_id):
            continue
        else:
            cart_id+=1
            print(cart_id)
    print(status)
    loop = len(ProductID)
    for i in range(0,loop):
        try:
            cur.execute('INSERT INTO ProductCart(CartID, MerchantID, ProductID, Status, Price, Information, Quantity) VALUES(%s,%s,%s,%s,%s,%s,%s)',(cart_id,merchant_id,ProductID[i],status,Price[i],Description[i],qty[i]))
            mysql.connection.commit()
        except Exception as e:
            print("Problem in inseting into db"+str(e))
            return None
    cur.close()