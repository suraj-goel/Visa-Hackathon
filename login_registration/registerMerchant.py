import uuid


def checkIfExistingMerchant(mysql, merchantEmail):
  """
  :param mysql: object to connect to database
  :param merchantEmail: email address of merchant
  :return: False if email already exists in database and True if email is not in database
  """
  cursor = mysql.connection.cursor()
  query = "select * from Merchant where EmailID='{}';".format(merchantEmail)
  cursor.execute(query)
  u = cursor.fetchall()
  cursor.close()
  if len(u) == 0:
      return False
  else:
      return True


def registerNewMerchant(mysql, email, password, merchantName, address, contactNumber, registeredName):
  """
  :param mysql: object to connect to database
  :param email: email address of merchant
  :param password: password choosen by merchant
  :param merchantName: name of merchant
  :param address: door address of merchant
  :param contactNumber: mobile number
  :param registeredName: name registered with visa
  :return: adds new merchant details to database and returns unique merchant identifier
  """
  id = str(uuid.uuid1().int)
  id = id[:19]
  address = address[:100]
  cur = mysql.connection.cursor()
  query = """INSERT INTO Merchant (MerchantID,Name,RegisteredName,EmailID,ContactNumber,Address,Password)VALUES(%s, 
  %s, %s, %s, %s, %s, %s); """
  cur.execute(query, (id, merchantName, registeredName, email, contactNumber, address, password))
  mysql.connection.commit()
  cur.close()
  return id


def checkPayType(mysql, merchantid):
  """
  :param mysql: object to connect to database
  :param merchantid: unique merchant identifier
  :return: if payment type is 3, returns true else false
  Payment Type 1 : only cybersource done
  Payment Type 2: only B2B registration done
  Payment Type 3: both are complete
  Both registration is required to create a merchant account
  """
  cur = mysql.connection.cursor()
  query = "select * from PaymentType where MerchantID='{}';".format(merchantid)
  cur.execute(query)
  result = cur.fetchone()
  cur.close()
  if result:
      if result['PayType'] == '3':
          return True
  else:
      return False


def insertLocation(mysql, lat, long, mid):
  """
  :param mysql: sql connection object
  :param lat, long: coordinates of location
  :param mid: unique merchant id
  adds merchant location details to database
  """
  id = str(uuid.uuid1().int)
  id = id[:20]
  cur = mysql.connection.cursor()
  query = """INSERT INTO Location (LocationID,Latitude,Longitude,MerchantID)VALUES(%s, %s, %s, %s);"""
  cur.execute(query, (id, lat, long, mid))
  mysql.connection.commit()
  cur.close()


def updateLocation(mysql, lat, long, mid):
    """
  :param mysql: object to connect to database
  :param lat, long: coordinates
  :param mid: unique merchant identifier
  updates merchant location
  """
    id = str(uuid.uuid1().int)
    id = id[:20]
    cur = mysql.connection.cursor()
    cur.execute(
        f"""UPDATE Location SET LocationID="{id}", Latitude="{lat}", Longitude="{long}" where MerchantID="{mid}";""")
    mysql.connection.commit()
    cur.close()
