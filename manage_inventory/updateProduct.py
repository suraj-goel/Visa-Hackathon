def updateProduct(productID,mysql,name,description,price,quantity,category,SellStatus):
    """
    :param productID: unique product identifier
    :param mysql: database connection object
    :param name: updated name of product
    :param description: updated description of product
    :param price: updated price of product
    :param quantity: updated quantity of product
    :param category: updated category of product
    :param SellStatus: updated status 1 indicates that supplier merchant wants to sell the product and 0 indicated that
                        supplier merchant does not want to sell the products
    :return: updates the product details using above parameters and returns "yes" if successful
    """
    db = mysql.connection
    cur = db.cursor()
    query = "Update Product SET Name = '{}', Description = '{}', Price ='{}', Quantity='{}', Category = '{}', Sell='{}' " \
            "WHERE ProductID = '{}' ".format(name,description,price,quantity,category,SellStatus,productID)
    
    cur.execute(query)
    db.commit()
    return "yes"
   

