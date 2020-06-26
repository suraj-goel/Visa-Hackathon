##   SUPPLIER SIDE    ##
# Received request posted by others
# proposal button can be added here and then we can add to RequirementAccepted database
# proposal accepts productid of only those that are sold by him
def RequestsApproved(mysql,merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Product where Product.ProductID=RequirementAccepted.ProductID "
                "and Requirement.RequirementID=RequirementAccepted.RequirementID and Product.MerchantID='%s';", (merchantid,))
    approved = cur.fetchall()
    return approved

def RequestsReceived(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement where MerchantID <> '%s' and Status='Post';", (merchantid,))
    posts = cur.fetchall()
    return posts


# Accepted request posted by others accepted by you
# here supplier waits for buyer to approve
def RequestsReceivedAndAccepted(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Product where Product.ProductID="
                "RequirementAccepted.ProductID and Requirement.RequirementID=RequirementAccepted.RequirementID and "
                "Product.MerchantID='%s' and RequirementAccepted.Status='yes';",(merchantid,))
    accepted_requests=cur.fetchall()
    return accepted_requests


# Rejected approval posted by others
def RequestsReceivedAndRejected(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Product where Product.ProductID=RequirementAccepted.ProductID "
                "and Requirement.RequirementID=RequirementAccepted.RequirementID and Product.MerchantID='%s' and "
                "Requirement.Status='Approved' and RequirementAccepted.Status='no';",(merchantid,))
    rejected=cur.fetchall()
    return rejected


def RequestsRecievedAndPending(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Product where Product.ProductID=RequirementAccepted.ProductID "
                "and Requirement.RequirementID=RequirementAccepted.RequirementID and Product.MerchantID='%s' and "
                "Requirement.Status='Post';", (merchantid,))
    pending = cur.fetchall()
    print(pending)
    return pending


##  BUYER SIDE  ##
# Status of request posted by you
# here i am showing history as well....we can remove it and add in order history or keep in both
# can create new filter for status as well
def PostedAndPending(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement where MerchantID = '%s' and Requirement.Status='Post';", (merchantid,))
    requirements_posted = cur.fetchall()
    if not requirements_posted:
        message = 'No requirements were posted by you'
        print(message)
        return None
    else:
        data_res = []
        for i in requirements_posted:
            res = i
            # retreive all accepts in case the requirement is still under post
            cur.execute("select * from Requirement,RequirementAccepted,Merchant,Product where Requirement.RequirementID="
                        "RequirementAccepted.RequirementID and Merchant.MerchantID=Product.MerchantID and Product.ProductID="
                        "RequirementAccepted.ProductID and Requirement.Status='Post' and Requirement.MerchantID ='%s' and "
                        "Requirement.RequirementID=%s;",(merchantid, str(i['RequirementID'])))
            x = cur.fetchall()
            # if no one accepted, dont add accept list to dictionary
            if x:
                data = []
                for j in x:
                    data.append(j)
                res['Accepts'] = data
            data_res.append(res)
        return data_res


# requirements posted by you and approved by others and accepted by you and paid and u are waiting for delivery
# when u accept update
# Requirement status as 'Approved'
# RequirementsAccepted status as 'yes' for that merchant
def PostedAndPaid(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Merchant,Product where "
                "Requirement.RequirementID=RequirementAccepted.RequirementID and Merchant.MerchantID=Product.MerchantID "
                "and Product.ProductID=RequirementAccepted.ProductID and RequirementAccepted.Status='yes' and "
                "Requirement.Status='Approved' and Requirement.MerchantID='%s';", (merchantid,))
    out_for_delivery = cur.fetchall()
    return out_for_delivery


def PostedAndDelivered(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Merchant,Product where "
                "Requirement.RequirementID=RequirementAccepted.RequirementID and Merchant.MerchantID=Product.MerchantID "
                "and Product.ProductID=RequirementAccepted.ProductID and RequirementAccepted.Status='yes' and "
                "Requirement.Status='Delivered' and Requirement.MerchantID='%s';", (merchantid,))
    delivered = cur.fetchall()
    return delivered

def getSupplierRequests(mysql,merchantid,choice='P'):
    if choice=='P':
        return RequestsReceived(mysql,merchantid)
    elif choice=='A':
        return RequestsReceivedAndAccepted(mysql,merchantid)
    elif choice=='W':
        return RequestsRecievedAndPending(mysql,merchantid)
    elif choice=='R':
        return RequestsReceivedAndRejected(mysql,merchantid)
    elif choice=='E':
        return RequestsApproved(mysql,merchantid)

def getBuyerRequests(mysql,merchantid,choice='R'):
    if choice=='R':
        return PostedAndPending(mysql,merchantid)
    elif choice=='P':
        return PostedAndPaid(mysql,merchantid)
    elif choice=='D':
        return PostedAndDelivered(mysql,merchantid)
    elif choice=='E':
        res=[]
        res.extend(PostedAndPending(mysql,merchantid))
        res.extend(PostedAndPaid(mysql,merchantid))
        res.extend(PostedAndDelivered(mysql,merchantid))
        return res


#SUPPLIER
def approveDeal(mysql,requirementID,merchantIDWhoPosted):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE RequirementAccepted,Requirement SET RequirementAccepted.Status='{}' WHERE RequirementAccepted.RequirementID='{}' AND Requirement.RequirementID='{}' AND Requirement.MerchantID='{}'".format("yes",requirementID,requirementID,merchantIDWhoPosted))
    mysql.connection.commit()


#BUYER
#ONLY AFTER PAYMENT
def acceptDeal(mysql,requirementID,merchantIDwhoPost,cartID):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Requirement,RequirementAccepted,Cart,Orders SET Requirement.Status= '{}' where Requirement.RequirementID='{}' and Orders.CartID='{}' and Requirement.MerchantID".format("Done",requirementID,cartID,merchantIDwhoPost))
    mysql.connection.commit()


#SUPPLIER
def rejectDeal(mysql,requirementID,merchantIDWhoPosted):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE RequirementAccepted,Requirement SET RequirementAccepted.Status='{}' WHERE RequirementAccepted.RequirementID='{}' AND Requirement.RequirementID='{}' AND Requirement.MerchantID='{}'".format("no",requirementID,requirementID,merchantIDWhoPosted))
    mysql.connection.commit()


#SUPPLIER
def allProductID(mysql,merchantID):
    cur = mysql.connection.cursor()
    cur.execute("select * from Product where Sell=1 and MerchantID='{}'".format(merchantID))
    sellProduct = list(cur.fetchall())
    return sellProduct



# product name = sellProduct[i]['Name']
# Price = sellProduct[i]['Price']
#Quantity = sellProduct[i]['Quantity']


