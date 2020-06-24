def getOrders(mysql,merchantid):
    cur=mysql.connection.cursor()
    cur.execute("select distinct * from Orders, Cart where Orders.CartID=Cart.CartID and Cart.MerchantID="+str(merchantid))
    carts=cur.fetchall()
    res=[]
    for i in carts:
        data=i
        cartid=i['CartID']
        cur.execute("select * from Cart,Product,ProductCart where Product.ProductID=ProductCart.ProductID and ProductCart.CartID=Cart.CartID and Cart.CartID='"+str(cartid)+"';")
        data['Products_list']=list(cur.fetchall())
        res.append(data)
    print(data)

def getRequirements():
    pass