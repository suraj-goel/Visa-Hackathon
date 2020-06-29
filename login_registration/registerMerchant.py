import random


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
  id = random.randint(1,1000)
  id = str(id)
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
  cur = mysql.connection.cursor()
  query = "select * from PaymentType where MerchantID='{}';".format(id)
  cur.execute(query)
  u = cur.fetchall()
  if len(u) == 0:
    return False
  else:
    return True








    
