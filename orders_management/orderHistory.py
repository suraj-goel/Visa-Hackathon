from manage_inventory.buyerUpdater import updateBuyerInventoryOrder
import uuid


def getOrders(mysql, merchantid, delivered_filter):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identification number
    :param delivered_filter: filter that can be
    'yes' - orders that were delivered
    'no' - orders that are yet to be delivered
    'all' - all orders
    :return: list of orders, delivery status, ratings posted by the buyer merchant and product details of the order
    """
    cur = mysql.connection.cursor()
    if delivered_filter == 'all':
        cur.execute("select distinct * from Orders, Cart where Orders.CartID=Cart.CartID and Cart.MerchantID=" + str(
            merchantid))
    elif delivered_filter == 'no':
        cur.execute("select distinct * from Orders, Cart where Orders.CartID=Cart.CartID and Orders.DeliveredDate "
                    "is null and Cart.MerchantID=" + str(merchantid))
    else:
        cur.execute("select distinct * from Orders, Cart where Orders.CartID=Cart.CartID and Orders.DeliveredDate "
                    "is not null and Cart.MerchantID=" + str(merchantid))
    carts = cur.fetchall()
    res = []
    for i in carts:
        data = i
        cartid = i['CartID']
        cur.execute("select * from Cart,Product,ProductCart where Product.ProductID=ProductCart.ProductID and "
                    "ProductCart.CartID=Cart.CartID and Cart.CartID='" + str(cartid) + "';")
        products = cur.fetchall()
        data['Products_list'] = list(products)
        cur.execute("select * from Merchant where MerchantID=%s;", (products[0]['Product.MerchantID'],))
        merchant_info = cur.fetchone()
        data['Merchant_Ordered'] = merchant_info
        if IsRated(mysql, i['OrderID']):
            data['Rated'] = IsRated(mysql, i['OrderID'])
        res.append(data)
    return res


def Delivered(mysql, orderid, merchantid):
    """
    :param mysql: database connection object
    :param orderid: unique order identification number
    :param merchantid: unique merchant identification number
    sets status to delivered and updates buyer inventory
    """
    cur = mysql.connection.cursor()
    cur.execute("update Orders set DeliveredDate=CURDATE() WHERE OrderID=%s;", (orderid,))
    mysql.connection.commit()
    updateBuyerInventoryOrder(mysql, orderid, merchantid)


def IsRated(mysql, orderid):
    """
    :param mysql: database connection object
    :param orderid: unique order identification number
    :return: returns ratings if present for the orderid and False if not already rated
    """
    cur = mysql.connection.cursor()
    cur.execute("select * from Ratings where OrderID=%s", (orderid,))
    ratings = cur.fetchone()
    if ratings:
        return ratings['Value']
    return False


def AddRating(mysql, orderid, rating):
    """
    :param mysql: database connection object
    :param orderid: unique order identification number
    :param rating: rating number out of 5
    adds ratings to database
    """
    cur = mysql.connection.cursor()
    cur.execute("insert into Ratings values (%s,%s,%s)", (uuid.uuid1(), orderid, rating))
    mysql.connection.commit()


# average rating for every merchant id
def SearchRatings(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identification number
    :return: list of ratings averaged for every merchant
    """
    cur = mysql.connection.cursor()
    cur.execute("select FLOOR(AVG(distinct Ratings.Value)+0.5) as stars ,Count(distinct Ratings.Value) as Votes, "
                "AVG(distinct Ratings.Value) as Avg_rating from Ratings,Orders,Cart,ProductCart,Product where "
                "Orders.OrderID=Ratings.OrderID and Cart.CartID=Orders.CartID and ProductCart.CartID=Cart.CartID and "
                "Product.ProductID=ProductCart.ProductID and Product.MerchantID=%s;", (merchantid,))
    ratings = cur.fetchone()
    return ratings
