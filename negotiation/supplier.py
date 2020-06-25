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

