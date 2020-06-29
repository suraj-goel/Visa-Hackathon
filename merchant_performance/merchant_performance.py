from services.visa_api_services import MerchantMeasurement


def getPerformanceStats(mysql,merchantid):
    data=getCategoryPerformance()
    data['total_spendings']=TotalSpendings(mysql,merchantid)
    data['total_earnings'] = TotalEarnings(mysql, merchantid)
    data['total_spendings_monthly']=TotalSpendings(mysql,merchantid)

    return data

def TotalSpendings(mysql,merchantid):
    cur=mysql.connection.cursor()
    cur.execute("select SUM(Total) as Total from Cart where MerchantID = %s;",(merchantid))
    return cur.fetchone()['Total']

def TotalSpendingsMonthly(mysql,merchantid):
    cur=mysql.connection.cursor()
    cur.execute("select SUM(Total) as Total from Cart where MerchantID = %s;",(merchantid))
    return cur.fetchone()['Total']

def TotalEarnings(mysql,merchantid):
    cur=mysql.connection.cursor()
    cur.execute("select Sum(A.Total) as Total from (select distinct Cart.CartID,Total from Cart,ProductCart,Product,Orders where "
                "Cart.CartID=ProductCart.CartID and ProductCart.ProductID=Product.ProductID and Orders.CartID=Cart.CartID"
                " and Product.MerchantID=%s) as A;",(merchantid))
    return cur.fetchone()['Total']

def getCategoryPerformance():
    data = MerchantMeasurement()
    return data

