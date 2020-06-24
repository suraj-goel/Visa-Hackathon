import uuid
def updateProduct(productID,merchantID,mysql,name,description,price,quantity,category,SellStatus):
    db = mysql.connection
    cur = db.cursor()
    sell = "0"
    if(SellStatus):
        sell="1"
    query = "Update Product SET Name = '{}', Description = '{}', Price ='{}', Quantity='{}', Category = '{}', Sell='{}' WHERE ProductID = '{}' ".format(name,description,price,quantity,category,sell,productID)
    
    cur.execute(query)
    db.commit()
    return "Success"
   

