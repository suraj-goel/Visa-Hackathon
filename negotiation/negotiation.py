

def displayAllNegotiation(mysql,merchant_id):
    cur = mysql.connection.cursor()
    cur.execute('select CartID from Cart where MerchantID = %s',(str(merchant_id)))
    a = cur.fetchall()
    negotiationCollection = []
    length = len(a)
    #print(a)
    for i in range(0,length):
        x = a[i]['CartID']
        try:
            cur.execute("select * from Negotiation where CartID='{}' and Status='{}'".format(a[i]['CartID'],'pending'))

        except Exception as e:
            print(e)
        b = cur.fetchall()
        negotiationCollection.append(b)
    return negotiationCollection


def diplayNegotiationType(mysql,merchant_id,status):
    cur = mysql.connection.cursor()
    cur.execute('select CartID from Cart where MerchantID = %s',(str(merchant_id)))
    a = cur.fetchall()
    negotiationCollection = []
    length = len(a)
    for i in range(0,length):
        cur.execute("select * from Negotiation where CartID='{}' and Status='{}'".format(a[i]['CartID'],status))
        negotiationCollection.append(cur.fetchall())
    return negotiationCollection

def deleteNegotiation(mysql,merchant_id,cart_id):
    cur = mysql.connection.cursor()
    cur.execute('delete from Negotiation where CartID=%s and Status=%s',('cart_id',"pending"))
    mysql.connection.commit()

def editNegotiation(mysql,merchant_id,cart_id,price):
    pass


def confirmNegotiation(mysql,negotiationID):
    cur = mysql.connection.cursor()
    cur.execute("Update Negotiation SET Status = 'accept' WHERE NegotiationID = '{}' ".format(negotiationID))
    mysql.connection.commit()
    return "Success"

def rejectNegotiation(mysql,negotiationID):
    cur = mysql.connection.cursor()
    cur.execute("Update Negotiation SET Status = 'reject' WHERE NegotiationID = '{}' ".format(negotiationID))
    mysql.connection.commit()
    return "Success"

