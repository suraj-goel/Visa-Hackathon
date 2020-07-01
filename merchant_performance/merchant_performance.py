from services.visa_api_services import MerchantMeasurement


def getPerformanceStats(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: performance data corresponding to merchant
    """
    data = getCategoryPerformance(mysql, merchantid)
    data['total_spendings'] = TotalSpendings(mysql, merchantid)
    data['total_earnings'] = TotalEarnings(mysql, merchantid)
    data['total_spendings_monthly'] = TotalSpendingsMonthly(mysql, merchantid)
    data['total_earnings_monthly'] = TotalEarningsMonthly(mysql, merchantid)
    data['total_trasactions'] = TotalTransaction(mysql, merchantid)
    data['total_transactions_monthly'] = TotalTransactionsMonthnly(mysql, merchantid)
    return data


def TotalSpendings(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: total spendings made by merchant on products purchased
    """
    cur = mysql.connection.cursor()
    cur.execute("select SUM(Total) as Total from Cart where MerchantID = %s;", (merchantid,))
    return cur.fetchone()['Total']


def TotalSpendingsMonthly(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: list of monthly spendings made sorted by month
    """
    cur = mysql.connection.cursor()
    cur.execute(
        "select sum(Total) as Total ,DATE_FORMAT(OrderedDate, '%m-%Y') as month from Cart,Orders where MerchantID =" + merchantid +
        " and Cart.CartID=Orders.CartID group by month;")
    res = cur.fetchall()
    return res


def TotalEarnings(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: total earnings made by merchant on products sold
    """
    cur = mysql.connection.cursor()
    cur.execute(
        "select Sum(A.Total) as Total from (select distinct Cart.CartID,Total from Cart,ProductCart,Product,Orders where "
        "Cart.CartID=ProductCart.CartID and ProductCart.ProductID=Product.ProductID and Orders.CartID=Cart.CartID"
        " and Product.MerchantID=%s) as A;", (merchantid,))
    return cur.fetchone()['Total']


def TotalEarningsMonthly(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: list of monthly earnings made sorted by month
    """
    cur = mysql.connection.cursor()
    cur.execute(
        "select sum(Total) as Total ,month from (select distinct Cart.CartID,Total,DATE_FORMAT(OrderedDate, '%m-%Y') as month "
        "from Cart,ProductCart,Product,Orders where Cart.CartID=ProductCart.CartID and ProductCart.ProductID=Product.ProductID"
        " and Orders.CartID=Cart.CartID and Product.MerchantID=" + merchantid + " ) as A group by month order by month;")
    return cur.fetchall()


def TotalTransaction(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: transactions completed by the supplier
    """
    cur = mysql.connection.cursor()
    cur.execute("select COUNT(distinct OrderID) as Orders from Orders,Cart,ProductCart,Product where Orders.CartID="
                "Cart.CartID and ProductCart.CartID=Cart.CartID and ProductCart.ProductID=Product.ProductID and "
                "Product.MerchantID=%s;", (merchantid,))
    return cur.fetchone()['Orders']


def TotalTransactionsMonthnly(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: list of monthly transactions made sorted by month
    """
    cur = mysql.connection.cursor()
    cur.execute(
        "select COUNT(distinct OrderID) as orders ,DATE_FORMAT(OrderedDate, '%m-%Y') as month  from Orders,Cart,"
        "ProductCart,Product where Orders.CartID=Cart.CartID and ProductCart.CartID=Cart.CartID and ProductCart."
        "ProductID=Product.ProductID and Product.MerchantID=" + merchantid + " group by month order by month;")
    return cur.fetchall()


def getCategoryPerformance(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: performance data returned by merchant measurement API
    """
    cur = mysql.connection.cursor()
    cur.execute("select MCC from Merchant where MerchantID=%s", (merchantid,))
    mcc = cur.fetchone()['MCC']
    cur.close()
    data = MerchantMeasurement(mcc)
    name = getCategoryName(mysql, mcc)
    data['category_name'] = name
    return data


def getCategoryName(mysql, mcc):
    """
    :param mysql: database connection object
    :param mcc: merchant category code
    :return: category name corresponding to merchant category code
    """
    cur = mysql.connection.cursor()
    cur.execute("select Category from MerchantCategoryCode where Code=%s;", (mcc,))
    category = cur.fetchone()['Category']
    cur.close()
    return category
