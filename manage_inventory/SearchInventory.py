def getAllProducts(mysql,merchantID,filter='A'):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM Product,Merchant WHERE Product.MerchantID =Merchant.MerchantID AND Merchant.MerchantID = " + str(1)
    cur.execute(query)
    a=list(cur.fetchall())
    return a