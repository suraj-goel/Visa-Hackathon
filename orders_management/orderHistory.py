def getOrders(mysql,merchantid,delivered_filter):
    cur=mysql.connection.cursor()
    if delivered_filter=='all':
        cur.execute("select distinct * from Orders, Cart where Orders.CartID=Cart.CartID and Cart.MerchantID="+str(merchantid))
    elif delivered_filter=='no':
        cur.execute("select distinct * from Orders, Cart where Orders.CartID=Cart.CartID and Orders.Status='no' and Cart.MerchantID=" + str(
            merchantid))
    else:
        cur.execute("select distinct * from Orders, Cart where Orders.CartID=Cart.CartID and Orders.Status='yes' and Cart.MerchantID=" + str(
            merchantid))
    carts=cur.fetchall()
    res=[]
    for i in carts:
        data=i
        cartid=i['CartID']
        cur.execute("select * from Cart,Product,ProductCart where Product.ProductID=ProductCart.ProductID and ProductCart.CartID=Cart.CartID and Cart.CartID='"+str(cartid)+"';")
        data['Products_list']=list(cur.fetchall())
        res.append(data)
    return res

def getRequirements():
    pass