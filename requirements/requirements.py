import uuid


def saveRequirements(mysql, merchantID, title, description, quantity, price, status):
    cur = mysql.connection.cursor()
    requirementId = uuid.uuid1()
    if description == "":
        description = title
    try:
        cur.execute(
            'insert into Requirement(requirementid, title, description, status, merchantid, price, quantity) VALUES(%s,%s,%s,%s,%s,%s,%s)',
            (requirementId, title, description, status, merchantID, price, quantity))
        mysql.connection.commit()
    except Exception as e:
        print("problem in inserting in db" + str(e))
        return None
    print("everything is fine")
    cur.close()


def showBusinessName(mysql, merchantID):
    cur = mysql.connection.cursor()
    cur.execute("select RegisteredName from Merchant where MerchantID='{}'".format(merchantID))
    a = cur.fetchall()
    return a[0]['RegisteredName']
