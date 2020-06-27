##   SUPPLIER SIDE    ##
# Received request posted by others
# proposal button can be added here and then we can add to RequirementAccepted database
# proposal accepts productid of only those that are sold by him

# all open posts
def RequestsReceived(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement as R, Merchant where R.Status='Post' and Merchant.MerchantID=R.MerchantID and R.MerchantID <> '%s' and "
                "NOT EXISTS( select * from RequirementAccepted where RequirementAccepted.RequirementID=R.RequirementId "
                "and RequirementAccepted.Status='yes');", (merchantid,))
    posts = cur.fetchall()
    for i in range(len(posts)):
        posts[i]['Status'] = 'Open'
    return posts

# all those posts that were approved by you
def RequestsApproved(mysql,merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Product,Merchant where Product.ProductID="
                "RequirementAccepted.ProductID and Requirement.RequirementID=RequirementAccepted.RequirementID and "
                "Product.MerchantID='%s' and Merchant.MerchantID=Requirement.MerchantID;", (merchantid,))
    approved = cur.fetchall()
    for i in range(len(approved)):
        approved[i]['Status'] = 'Approved by you'
    return approved


# Accepted by buyer
def RequestsReceivedAndAccepted(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Product,Merchant where Product.ProductID="
                "RequirementAccepted.ProductID and Requirement.RequirementID=RequirementAccepted.RequirementID and "
                "Product.MerchantID='%s' and Requirement.Status='Done' and RequirementAccepted.Status='yes' and "
                "Merchant.MerchantID=Requirement.MerchantID;",(merchantid,))
    accepted_requests=cur.fetchall()
    for i in range(len(accepted_requests)):
        accepted_requests[i]['Status'] = 'Buyer accepted and paid'
    return accepted_requests


# Rejected approvals of yours
def RequestsReceivedAndRejected(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Product,Merchant where Product.ProductID=RequirementAccepted.ProductID "
                "and Requirement.RequirementID=RequirementAccepted.RequirementID and Product.MerchantID='%s' and "
                "Requirement.Status='Done' and RequirementAccepted.Status='no' and Merchant.MerchantID=Requirement.MerchantID;",(merchantid,))
    rejected=cur.fetchall()
    for i in range(len(rejected)):
        rejected[i]['Status'] = 'Rejected and closed'
    return rejected

# posts accepted by you but no response
def RequestsRecievedAndPending(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Product,Merchant where Product.ProductID=RequirementAccepted.ProductID "
                "and Requirement.RequirementID=RequirementAccepted.RequirementID and Product.MerchantID='%s' and "
                "Requirement.Status='Post' and Merchant.MerchantID=Requirement.MerchantID;", (merchantid,))
    pending = cur.fetchall()
    for i in range(len(pending)):
        pending[i]['Status'] = 'Waiting for buyer response'
    return pending

def getSupplierRequests(mysql,merchantid,choice='P'):
    merchantid=int(merchantid)
    if choice=='P':
        return RequestsReceived(mysql,merchantid)
    elif choice=='A':
        return RequestsReceivedAndAccepted(mysql,merchantid)
    elif choice=='W':
        return RequestsRecievedAndPending(mysql,merchantid)
    elif choice=='R':
        return RequestsReceivedAndRejected(mysql,merchantid)
    elif choice=='E':
        res=list(RequestsRecievedAndPending(mysql,merchantid))
        res.extend(RequestsReceivedAndAccepted(mysql,merchantid))
        res.extend(RequestsReceivedAndRejected(mysql,merchantid))
        return res

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
            # if no one accepted, then it is in pending state
            if not x:
                data_res.append(res)
        for i in range(len(data_res)):
            data_res[i]['Status'] = 'Pending'
        return data_res


# requirements posted by you and approved by others and accepted by you and paid and u are waiting for delivery
# Requirement status as 'Done'
# RequirementsAccepted status as 'yes' for that merchant
# the info is now visible in order table
def PostedAndAcceptedBySupplier(mysql, merchantid):
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
            cur.execute(
                "select * from Requirement,RequirementAccepted,Merchant,Product where Requirement.RequirementID="
                "RequirementAccepted.RequirementID and Merchant.MerchantID=Product.MerchantID and Product.ProductID="
                "RequirementAccepted.ProductID and Requirement.Status='Post' and Requirement.MerchantID ='%s' and "
                "Requirement.RequirementID=%s;", (merchantid, str(i['RequirementID'])))
            x = cur.fetchall()
            # if no one accepted, dont add accept list to dictionary
            if x:
                data = []
                for j in x:
                    data.append(j)
                res['Accepts'] = data
                data_res.append(res)
        for i in range(len(data_res)):
            data_res[i]['Status'] = 'Accepted'
        return data_res

def PostedAndDone(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Merchant,Product where "
                "Requirement.RequirementID=RequirementAccepted.RequirementID and Merchant.MerchantID=Product.MerchantID "
                "and Product.ProductID=RequirementAccepted.ProductID and RequirementAccepted.Status='yes' and "
                "Requirement.Status='Done' and Requirement.MerchantID='%s';", (merchantid,))
    delivered = cur.fetchall()
    for i in range(len(delivered)):
        delivered[i]['Status']='Done'
    return delivered

def getBuyerRequests(mysql,merchantid,choice='R'):
    merchantid=int(merchantid)
    if choice=='R':
        return PostedAndPending(mysql,merchantid)
    elif choice=='A':
        return PostedAndAcceptedBySupplier(mysql,merchantid)
    elif choice=='D':
        return PostedAndDone(mysql,merchantid)
    elif choice=='E':
        res=[]
        res.extend(PostedAndPending(mysql,merchantid))
        res.extend(PostedAndAcceptedBySupplier(mysql,merchantid))
        res.extend(PostedAndDone(mysql,merchantid))
        return res


#SUPPLIER
def approveDeal(mysql,requirementID,productID):

    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO RequirementAccepted values('{}','{}','{}')".format(requirementID,productID,"no"))
    except Exception as e:
        print("insert "+str(e))

    cur.execute("UPDATE RequirementAccepted,Requirement SET RequirementAccepted.Status='{}'  WHERE RequirementAccepted.RequirementID='{}' AND Requirement.RequirementID='{}'".format("yes",requirementID,requirementID,))
    mysql.connection.commit()
    cur.execute("UPDATE RequirementAccepted,Requirement SET RequirementAccepted.ProductID='{}'  WHERE RequirementAccepted.RequirementID='{}' AND Requirement.RequirementID='{}'".format(productID,requirementID,requirementID))
    mysql.connection.commit()


#BUYER
#ONLY AFTER PAYMENT
def acceptDeal(mysql,requirementID,merchantIDwhoPost,cartID):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Requirement,RequirementAccepted,Cart,Orders SET Requirement.Status= '{}' where Requirement.RequirementID='{}' and Orders.CartID='{}' and Requirement.MerchantID".format("Done",requirementID,cartID,merchantIDwhoPost))

    mysql.connection.commit()


#SUPPLIER
def rejectDeal(mysql,requirementID):
    cur = mysql.connection.cursor()
    #cur.execute("UPDATE RequirementAccepted,Requirement SET RequirementAccepted.Status='{}' WHERE RequirementAccepted.RequirementID='{}' AND Requirement.RequirementID='{}'".format("no",requirementID,requirementID))
    try:
        cur.execute("INSERT INTO RequirementAccepted values('{}','{}','{}')".format(requirementID,"nothing","no"))
    except Exception as e:
        print("insert "+str(e))
    mysql.connection.commit()


#SUPPLIER
def allProductID(mysql,merchantID):
    cur = mysql.connection.cursor()
    cur.execute("select * from Product where Sell='1' and MerchantID='{}'".format(merchantID))
    sellProduct = list(cur.fetchall())
    #print(sellProduct)
    return sellProduct

#BUYER
def deletePending(mysql,requirementID):

    cur = mysql.connection.cursor()
    cur.execute("select * from RequirementAccepted where RequirementID='{}' and Status='{}'".format(requirementID,"yes"))
    a = cur.fetchall();
    loop = len(a)
    if(loop == 0):
        cur.execute("Delete from Requirement where RequirementID='{}'".format(requirementID))
        mysql.connection.commit()


def getInfo(mysql,requiremenID):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement where RequirementID='{}'".format(requiremenID))
    a=cur.fetchall()
    return a

# product name = sellProduct[i]['Name']
# Price = sellProduct[i]['Price']
#Quantity = sellProduct[i]['Quantity']


