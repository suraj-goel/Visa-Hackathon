'''
{"ProductID": ProductID,
"Quantity": number of product purchased
        }
'''

def updateSupplierInventory(mysql,productList):
    cur = mysql.connection.cursor()
    for i in productList:
        productid=i['ProductID']
        print(productid)
        cur.execute('select quantity from Product where productID="%s";',(productid,))
        quan=int(cur.fetchone()['quantity'])-int(i['Quantity'])
        cur.execute('update Product set Quantity="%s" where productID="%s";',(quan,productid))
        mysql.connection.commit()


