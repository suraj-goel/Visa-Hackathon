def checkEmailAndPassword(mysql,merchantEmail,merchantPassword):
  cursor = mysql.connection.cursor()
  query = 'select * from MERCHANT where email=%s and password=%s'
  cursor.execute(query, merchantEmail,merchantPassword)
  return cursor.fetchall()