import uuid


def updateBuyerInventoryOrder(mysql, orderID, buyerMerchantID):
    """
    :param mysql: database connection object
    :param orderID: unique order identifier
    :param buyerMerchantID: unique merchant identifier of the buyer
    :return: updates the inventory of buyer when order is correctly processed and returns "Success"
    """
    query = "SELECT Name , Description,Price,ProductCart.Quantity as Quantity,Category FROM Orders,ProductCart,Product " \
            "WHERE OrderID = '{}' AND Orders.CartID = ProductCart.CartID AND ProductCart.ProductID = Product.ProductID"\
        .format(orderID)
    cur = mysql.connection.cursor()
    cur.execute(query)
    res = list(cur.fetchall())
    for i in range(len(res)):
        name = res[i]["Name"]
        cur.execute("SELECT * FROM Product WHERE Name = '{}' AND MerchantID = '{}'".format(name, buyerMerchantID))
        product = list(cur.fetchall())
        if not product:
            # product does not exist in database hence add a new entry for the product
            uid = uuid.uuid1()
            insertQuery = "INSERT INTO Product VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(uid, name,
                res[i]["Description"],res[i]["Price"],res[i]["Quantity"],res[i]["Category"],buyerMerchantID, "0")
            cur.execute(insertQuery)
            mysql.connection.commit()
        else:
            # product exists in database hence update the quantity
            quantity = str(int(product[0]["Quantity"]) + int(res[i]["Quantity"]))
            updateQuery = "Update Product SET Quantity = '{}' WHERE ProductID = '{}'".format(quantity,
                                                                                             product[0]["ProductID"])
            cur.execute(updateQuery)
            mysql.connection.commit()
    cur.close()
    return "Success"


def updateBuyerInventoryRequirement(mysql, productID, buyerMerchantID):
    """
    :param mysql: database connection object
    :param productID: uniqure product identifier
    :param buyerMerchantID:  unique merchant identifier
    :return: updates buyer inventory when a requirement was processed and returns "Success"
    """
    query = "SELECT RequirementAccepted.ProductID,Quantity,Price FROM Requirement INNER JOIN RequirementAccepted ON " \
            "Requirement.RequirementID = RequirementAccepted.RequirementID WHERE RequirementAccepted.ProductID = '{}' " \
            "AND Requirement.MerchantID = '{}' AND RequirementAccepted.Status = 'yes' ".format(productID, buyerMerchantID)
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = list(cur.fetchall())
    cur.execute("SELECT * FROM Product WHERE ProductID = '{}'".format(productID))
    res = list(cur.fetchall())
    for i in range(len(res)):
        name = res[i]["Name"]
        cur.execute("SELECT * FROM Product WHERE Name = '{}' AND MerchantID = '{}'".format(name, buyerMerchantID))
        product = list(cur.fetchall())
        if not product:
            uid = uuid.uuid1()
            insertQuery = "INSERT INTO Product VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(uid, name,
                  res[i]["Description"],res[i]["Price"],res[i]["Quantity"],res[i][ "Category"],buyerMerchantID, "0")
            cur.execute(insertQuery)
            mysql.connection.commit()
        else:
            if not data[0]["Quantity"]:
                quantity = str(int(product[0]["Quantity"]) + int(res[i]["Quantity"]))
            else:
                quantity = str(int(product[0]["Quantity"]) + int(data[0]["Quantity"]))
            updateQuery = "Update Product SET Quantity = '{}' WHERE ProductID = '{}'".format(quantity,product[0]["ProductID"])
            cur.execute(updateQuery)
            mysql.connection.commit()
    cur.close()
    return "Success"
