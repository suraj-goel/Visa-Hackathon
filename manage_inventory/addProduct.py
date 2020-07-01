import uuid

def getCategories(mysql):
	"""
	:param mysql: database connection object
	:return: a list of available product categories
	"""
	cur = mysql.connection.cursor()
	cur.execute("select distinct Category from Product;")
	lis=[i['Category'] for i in list(cur.fetchall())]
	cur.close()
	return lis

def addNewProduct(name,description,price,quantity,category,sell,merchantID,mysql):
	"""
	:param name: product name
	:param description: product description
	:param price: price per unit of product in rupees
	:param quantity: quantity of products to be added to stock
	:param category: product category
	:param sell: flag used to distinguish between products that are sold or stored by merchant
	:param merchantID: unique merchant identifier
	:param mysql: databseconnection object
	:return: 'yes' if product was added succesfully 'no' if product could not be added
	"""
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
