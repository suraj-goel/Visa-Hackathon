def updateSupplierInventory(mysql,productList,qtyList):
    """
    :param mysql: database connection object
    :param productList: list of products in supplier stock that was purchased by buyer
    :param qtyList: quantity of products for each item in productList that was purchased
    updates supplier inventory by deducing purchased quantities for the purchased products
    """
    cur = mysql.connection.cursor()
    for i in range(len(productList)):
        productid = productList[i]
        qty = int(qtyList[i])
        if qty>0:
            cur.execute("select Quantity from Product where productID='"+productid+"';")
            result = int(cur.fetchone()["Quantity"]) - qty
            cur.execute("update Product set Quantity='"+str(result)+"' where productID='"+productid+"';")
            mysql.connection.commit()


