def validation(mysql,mid,mname,regname,email,contact,address,password):
	"""
		To perform validations on editing account details
		The details are entered in editAccountDetails.html by user
		Validations include checking if username, email, door address, shop registered name is already existing
	"""
	flag = [0,0,0,0,0]
	cur = mysql.connection.cursor()
	r = [{},[],0]
	cur.execute("select * from Merchant where MerchantID = '"+mid+"';")
	result = cur.fetchone()
	r[0] = result
	if result['Name']!=mname:
		cur.execute("select * from Merchant where Name ='"+mname+"';")
		res = cur.fetchone()
		if res != None:
			flag[0] = 1
		else:
			r[0]['Name'] = mname
	if result['RegisteredName'] != regname:
		if result['RegisteredName'] != regname:
			if "'" in regname:
				a, c = regname.split("'")
				regname = a+chr(39)+c
		cur.execute(f'''select * from Merchant where RegisteredName = "{regname}";''')
		res = cur.fetchone()
		if res != None:
			flag[1]=1
		else:
			r[0]['RegisteredName'] = regname
	if result['EmailID']!=email:
		cur.execute("select * from Merchant where EmailID ='"+email+"';")
		res = cur.fetchone()
		if res != None:
			flag[2]=1
		else:
			r[0]['EmailID'] = email
	if result['ContactNumber']!=contact:
		cur.execute("select * from Merchant where ContactNumber ='"+contact+"';")
		res = cur.fetchone()
		if res != None:
			flag[3]=1
		else:
			r[0]['ContactNumber'] = contact
	if result['Address']!=address:
		if result['Address'] != address:
			if "'" in address:
				a, c = address.split("'")
				address = a+chr(39)+c
		cur.execute(f'''select * from Merchant where Address = "{address}";''')
		res = cur.fetchone()
		if res != None:
			flag[4]=1
		else:
			r[0]['Address'] = address
	for i in flag:
		if i:
			r[2] = 1
	r[1] = flag
	cur.close()
	return r
