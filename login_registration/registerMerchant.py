#import random
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
  id = str(uuid.uuid1().int)
  id = id[:20]
  print(address)
  address = address[:100]
  print(address)
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
  result = cur.fetchone()
  if result:
    if result['PayType']=='3':
      return True
  else:
    return False

def insertLocation(mysql, lat, long, mid):
  id = str(uuid.uuid1().int)
  id = id[:20]
  print(id)
  cur = mysql.connection.cursor()
  # query = "select * from Merchant where EmailID='{}';".format(merchantEmail)
  query = """INSERT INTO Location (LocationID,Latitude,Longitude,MerchantID)VALUES(%s, %s, %s, %s);"""
  cur.execute(query, (id, lat, long, mid))
  mysql.connection.commit()
  cur.close()







    
