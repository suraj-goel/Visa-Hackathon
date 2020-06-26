from manage_inventory.buyerUpdater import updateBuyerInventoryOrder


def getOrders(mysql,merchantid,delivered_filter):
    cur=mysql.connection.cursor()
    if delivered_filter=='all':
        cur.execute("select distinct * from Orders, Cart where Orders.CartID=Cart.CartID and Cart.MerchantID="+str(merchantid))
    elif delivered_filter=='no':
        cur.execute("select distinct * from Orders, Cart where Orders.CartID=Cart.CartID and Orders.DeliveredDate is null and Cart.MerchantID=" + str(
            merchantid))
    else:
        cur.execute("select distinct * from Orders, Cart where Orders.CartID=Cart.CartID and Orders.DeliveredDate is not null and Cart.MerchantID=" + str(
            merchantid))
    carts=cur.fetchall()
    res=[]
    for i in carts:
        data=i
        cartid=i['CartID']
        cur.execute("select * from Cart,Product,ProductCart where Product.ProductID=ProductCart.ProductID and ProductCart.CartID=Cart.CartID and Cart.CartID='"+str(cartid)+"';")
        data['Products_list']=list(cur.fetchall())
        res.append(data)
    print(res)
    return res

def Delivered(mysql,orderid,merchantid):
    #updateBuyerInventoryOrder(mysql, orderid, merchantid)
    pass