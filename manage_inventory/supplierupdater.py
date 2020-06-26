'''
{"ProductID": ProductID,
"Quantity": number of product purchased
        }
'''

def updateSupplierInventory(mysql,productList,qtyList):
    cur = mysql.connection.cursor()
    #print(productList,qtyList)
    for i in range(len(productList)):
        productid = productList[i]
        qty = int(qtyList[i])
        if qty>0:
            cur.execute("select Quantity from Product where productID='"+productid+"';")
            result = int(cur.fetchone()["Quantity"]) - qty
            #print(result)
            cur.execute("update Product set Quantity='"+str(result)+"' where productID='"+productid+"';")
            mysql.connection.commit()


