def getAllProducts(mysql,merchantID,filter='A'):
    cur = mysql.connection.cursor()
    if filter=='S':
        query=''
    if filter=='N':
        query = ''
    if filter=='A':
        query = ''
    cur.execute(query)
    a=list(cur.fetchall())
    return a