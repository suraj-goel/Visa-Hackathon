import uuid


def checkIfExistingMerchant(mysql,merchantEmail):
  cursor = mysql.connection.cursor()
  query = "select * from Merchant where EmailID='{}';".format(merchantEmail)
  cursor.execute(query)
  u = cursor.fetchall()

  if len(u) == 0:
    return False
  else:
    return True

def registerNewMerchant(mysql, email, password, merchantName,address,contactNumber,registeredName):
  id = uuid.uuid1()
  print(id)
  print(email,password,merchantName,address,contactNumber,registeredName)
  cur = mysql.connection.cursor()
  #query = "select * from Merchant where EmailID='{}';".format(merchantEmail)
  query = """INSERT INTO Merchant (MerchantID,Name,RegisteredName,EmailID,ContactNumber,Address,Password)VALUES(%s, %s, %s, %s, %s, %s, %s);"""
  cur.execute(query, (id, merchantName, registeredName, email, contactNumber, address, password))
  mysql.connection.commit()
  cur.close()
  return id

def checkPayType(mysql,id):
  cursor = mysql.connection.cursor
  query = "select * from PaymentType where MerchantID='{}';".format(id)
  cursor.execute(query)
  u = cursor.fetchall()
  if len(u) == 0:
    return False
  else:
    return True








    
