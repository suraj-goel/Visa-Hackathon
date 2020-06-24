import uuid
def addNewProduct(name,description,price,quantity,category,SellStatus,merchantID,mysql):
	db = mysql.connection
	cur = mysql.connection.cursor()
	uid = uuid.uuid1()
	sell = "0"
	if(SellStatus):
		sell = "1"
	query = "INSERT INTO Product VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(uid,name,description,price,quantity,category,merchantID,sell)
	
	cur.execute(query)
	db.commit()
	return "Success" 
