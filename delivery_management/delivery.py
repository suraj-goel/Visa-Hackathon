def getDelivery(mysql, merchantid, delivered_filter):
    """
    :param mysql: object to connect to database
    :param merchantid: unique identifier for a merchant
    :param delivered_filter: user input to check orders that were delivered or pending delivery or view all orders
    :return: list of orders containing products ordered, ordered and delivery dates, supplier merchant information,
    rating for the order based on delivered_filter
    """
    cur = mysql.connection.cursor()
    if delivered_filter == 'all':
        cur.execute(
            "select distinct Merchant.Name ,Merchant.Address ,Merchant.RegisteredName, Merchant.ContactNumber,"
            "ProductCart.CartID,Orders.OrderID, Orders.DeliveredDate ,Orders.OrderedDate, Cart.Total from Cart, "
            "Orders,ProductCart,Product,Merchant where Cart.MerchantID=Merchant.MerchantID and "
            "Orders.CartID=ProductCart.CartID and ProductCart.ProductID= "
            "Product.ProductID and Product.MerchantID=%s and Cart.CartID=ProductCart.CartID", (merchantid,))
    elif delivered_filter == 'no':
        cur.execute(
            "select distinct Merchant.Name ,Merchant.Address ,Merchant.RegisteredName, Merchant.ContactNumber,"
            "ProductCart.CartID,Orders.OrderID, Orders.DeliveredDate ,Orders.OrderedDate, Cart.Total from Cart, "
            "Orders,ProductCart,Product,Merchant where Cart.MerchantID=Merchant.MerchantID and "
            "Orders.CartID=ProductCart.CartID and ProductCart.ProductID= Product.ProductID and Product.MerchantID=%s "
            "and Orders.DeliveredDate is null and Cart.CartID=ProductCart.CartID",(merchantid,))
    else:
        cur.execute(
            "select distinct Merchant.Name ,Merchant.Address ,Merchant.RegisteredName, Merchant.ContactNumber,"
            "ProductCart.CartID,Orders.OrderID, Orders.DeliveredDate ,Orders.OrderedDate,Cart.Total from Cart, "
            "Orders,ProductCart,Product,Merchant where Cart.MerchantID=Merchant.MerchantID and "
            "Orders.CartID=ProductCart.CartID and ProductCart.ProductID=Product.ProductID and Product.MerchantID=%s "
            "and Orders.DeliveredDate is not null and Cart.CartID=ProductCart.CartID",(merchantid,))
    res = []
    carts = cur.fetchall()
    for i in carts:
        data = i
        cartid = i['CartID']
        cur.execute(
            "select * from Cart,Product,ProductCart where Product.ProductID=ProductCart.ProductID and ProductCart.CartID=Cart.CartID and Cart.CartID='" + str(
                cartid) + "';")
        data['Products_list'] = list(cur.fetchall())
        if IsRated(mysql, i['OrderID']):
            data['Rated'] = IsRated(mysql, i['OrderID'])
        res.append(data)
    cur.close()
    return res


def IsRated(mysql, orderid):
    """
    :param mysql: to connect to database
    :param orderid: order identification number
    Checks if the order was rated by the buyer merchant
    :return: rating out of if it exists or false
    """
    cur = mysql.connection.cursor()
    cur.execute("select * from Ratings where OrderID=%s", (orderid,))
    a = cur.fetchone()
    cur.close()
    if a:
        return a['Value']
    return False


def YourRatings(mysql, merchantid):
    """
    :param mysql: object to connect to database
    :return: average rating of the merchant out of 5 using MerchantID
    """
    cur = mysql.connection.cursor()
    cur.execute("select FLOOR(AVG(distinct Ratings.Value)+0.5) as stars ,Count(distinct Ratings.Value) as Votes, "
                "AVG(distinct Ratings.Value) as Avg_rating from Ratings,Orders,Cart,ProductCart,Product where "
                "Orders.OrderID=Ratings.OrderID and Cart.CartID=Orders.CartID and ProductCart.CartID=Cart.CartID and "
                "Product.ProductID=ProductCart.ProductID and Product.MerchantID=%s;", (merchantid,))
    ratings = cur.fetchone()
    cur.close()
    return ratings
