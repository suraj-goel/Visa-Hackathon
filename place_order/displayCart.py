
def addToCart(mysql,qty,ProductID,Name,Description,Price,merchant_id,status,finalPrice,finalDiscountPrice):

    cur = mysql.connection.cursor()
    cur.execute("select CartID FROM Cart ORDER BY CartID")
    a=cur.fetchall()
    cart_id = 1

    for i in range(0,len(a)):
        if str(a[i]['CartID']) != str(cart_id):
            continue
        else:
            cart_id += 1
    try:
        cur.execute('INSERT INTO Cart(CartID, Total,Status, MerchantID) VALUES(%s,%s,%s,%s)',(cart_id,finalDiscountPrice,status,merchant_id))
    except Exception as e:
        print("Problem in inserting in db"+ str(e))
        return None
    loop = len(ProductID)
    for i in range(0,loop):
        try:
            cur.execute('INSERT INTO ProductCart(CartID, ProductID,Quantity) VALUES(%s,%s,%s)',(cart_id,ProductID[i],qty[i]))
            mysql.connection.commit()
        except Exception as e:
            print("Problem in inseting into db"+str(e))
            return None
    cur.close()