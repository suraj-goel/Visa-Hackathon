

def displayAllNegotiation(mysql,merchant_id):
    cur = mysql.connection.cursor()
    cur.execute('select CartID from Cart where MerchantID = %s',(str(merchant_id)))
    a = cur.fetchall()
    negotiationCollection = []
    length = len(a)
    for i in range(0,length):
        cur.execute('select * from Negotiation where CartID=%s',(a[i]['CartID']))
        negotiationCollection.append(cur.fetchall())
    return negotiationCollection


def diplayNegotiationType(mysql,merchant_id,status):
    cur = mysql.connection.cursor()
    cur.execute('select CartID from Cart where MerchantID = %s',(str(merchant_id)))
    a = cur.fetchall()
    negotiationCollection = []
    length = len(a)
    for i in range(0,length):
        cur.execute('select * from Negotiation where CartID=%s and Status=%s',(a[i]['CartID'],status))
        negotiationCollection.append(cur.fetchall())
    return negotiationCollection

def deleteNegotiation(mysql,merchant_id,cart_id):
    cur = mysql.connection.cursor()
    cur.execute('delete from Negotiation where CartID=%s and Status=%s',('cart_id',"pending"))
    mysql.connection.commit()

def editNegotiation(mysql,merchant_id,cart_id,price):
    pass
