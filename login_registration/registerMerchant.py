def checkIfExistingMerchant(mysql,merchantEmail):
  cursor = mysql.connection.cursor()
  query = 'select COUNT(*) from MERCHANT where email=%s'
  cursor.execute(query, merchantEmail)
  if next(cursor, None) is None:
    return False
  else:
    return True

def registerNewMerchant(mysql, email, password,name):
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
  cur.execute(query, (mID, mName, mRegisteredName, mEmailID, mContactNumber, mAddress, mPassword))
  mysql.connection.commit()
  cur.close()







    
