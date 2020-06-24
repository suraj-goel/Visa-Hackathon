import uuid

def getCategories(mysql):
	cur = mysql.connection.cursor()
	cur.execute("select distinct Category from Product;")
	lis=[i['Category'] for i in list(cur.fetchall())]
	return lis

def addNewProduct(name,description,price,quantity,category,sell,merchantID,mysql):
	cur = mysql.connection.cursor()
	uid = uuid.uuid1()
	cur.execute("select * from Product where Name=%s and merchantID=%s",(name,merchantID))
	x=cur.fetchall()
	if x:
		return 'no'
	query = "INSERT INTO Product VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(uid,name,description,price,quantity,category,merchantID,sell)
	cur.execute(query)
	mysql.connection.commit()
	return 'yes'
