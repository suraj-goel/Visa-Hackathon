import uuid


def checkIfExistingMerchant(mysql,merchantEmail):
  cursor = mysql.connection.cursor()
  query = 'select COUNT(*) from MERCHANT where email=%s'
  cursor.execute(query, merchantEmail)
  if next(cursor, None) is None:
    return False
  else:
    return True

def registerNewMerchant(mysql, email, password,name):
  id = uuid.uuid1()
  cur = mysql.connection.cursor
  query = """INSERT INTO 
        MERCHANT (
            MerchantID,
            Name,
            RegisteredName,
            EmailID,
            ContactNumber,
            Address,
            Password)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
  cur.execute(query, (id, name, mRegisteredName, email, mContactNumber, mAddress, password))
  mysql.connection.commit()
  cur.close()
  return id

def checkPayType(mysql,id):
  cur = mysql.connection.cursor
  query = "check if id has a fixed payment type in the table "
  cur.execute(query)
  if next(cur, None) is None:
    return False
  else:
    return True








    
