from orders_management.orderHistory import SearchRatings


##   SUPPLIER SIDE    ##
# Received request posted by others

def RequestsReceived(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: all open requirement posts
    """
    cur = mysql.connection.cursor()
    cur.execute(
        "select * from Requirement as R, Merchant where R.Status='Post' and Merchant.MerchantID=R.MerchantID and R.MerchantID <> '%s' and "
        "NOT EXISTS( select * from RequirementAccepted where RequirementAccepted.RequirementID=R.RequirementId "
        "and RequirementAccepted.Status='yes');", (merchantid,))
    posts = cur.fetchall()
    for i in range(len(posts)):
        posts[i]['Status'] = 'Open'
    return posts


def RequestsApproved(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: all open requirement posts approved by the merchant as a supplier
    """
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Product,Merchant where Product.ProductID="
                "RequirementAccepted.ProductID and Requirement.RequirementID=RequirementAccepted.RequirementID and "
                "Product.MerchantID='%s' and Merchant.MerchantID=Requirement.MerchantID;", (merchantid,))
    approved = cur.fetchall()
    for i in range(len(approved)):
        approved[i]['Status'] = 'Approved by you'
    return approved



def RequestsReceivedAndAccepted(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: all requirement posts that were approved by supplier and accepted by buyer
    """
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Product,Merchant where Product.ProductID="
                "RequirementAccepted.ProductID and Requirement.RequirementID=RequirementAccepted.RequirementID and "
                "Product.MerchantID='%s' and Requirement.Status='Done' and RequirementAccepted.Status='yes' and "
                "Merchant.MerchantID=Requirement.MerchantID;", (merchantid,))
    accepted_requests = cur.fetchall()
    for i in range(len(accepted_requests)):
        accepted_requests[i]['Status'] = 'Buyer accepted and paid'
    return accepted_requests


def RequestsReceivedAndRejected(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: all requirement posts that were approved by supplier and rejected by buyer
    """
    cur = mysql.connection.cursor()
    cur.execute(
        "select * from Requirement,RequirementAccepted,Product,Merchant where Product.ProductID=RequirementAccepted.ProductID "
        "and Requirement.RequirementID=RequirementAccepted.RequirementID and Product.MerchantID='%s' and "
        "Requirement.Status='Done' and RequirementAccepted.Status='no' and Merchant.MerchantID=Requirement.MerchantID;",
        (merchantid,))
    rejected = cur.fetchall()
    for i in range(len(rejected)):
        rejected[i]['Status'] = 'Rejected and closed'
    return rejected



def RequestsRecievedAndPending(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :return: all requirement posts that were approved by supplier and pending response from buyer
    """
    cur = mysql.connection.cursor()
    cur.execute(
        "select * from Requirement,RequirementAccepted,Product,Merchant where Product.ProductID=RequirementAccepted.ProductID "
        "and Requirement.RequirementID=RequirementAccepted.RequirementID and Product.MerchantID='%s' and "
        "Requirement.Status='Post' and Merchant.MerchantID=Requirement.MerchantID;", (merchantid,))
    pending = cur.fetchall()
    for i in range(len(pending)):
        pending[i]['Status'] = 'Waiting for buyer response'
    return pending


def getSupplierRequestsSearch(mysql, merchantid, search):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identifier
    :param search: product name for supplier to search
    :return: all open requirement posts matching the search
    """
    cur = mysql.connection.cursor()
    cur.execute(
        "select * from Requirement as R, Merchant where R.Status='Post' and Merchant.MerchantID=R.MerchantID and R.MerchantID <> %s and "
        "NOT EXISTS( select * from RequirementAccepted where RequirementAccepted.RequirementID=R.RequirementId "
        "and RequirementAccepted.Status='yes') and R.Title like %s;", (merchantid, '%' + search + '%'))
    posts = cur.fetchall()
    for i in range(len(posts)):
        posts[i]['Status'] = 'Open'
    return posts


def getSupplierRequests(mysql, merchantid, choice='P'):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identification number for the supplier
    :param choice: filter to get requirements
    1. P : open requirements
    2. A : requirements approved by supplier and accepted by buyer
    3. W : requirements approved by supplier and pending buyer response
    4. R : requirements approved by suppllier and rejected by buyer
    5. E : all approved requirements by supplier
    :return: list of requirements based on filter
    """
    merchantid = int(merchantid)
    if choice == 'P':
        return RequestsReceived(mysql, merchantid)
    elif choice == 'A':
        return RequestsReceivedAndAccepted(mysql, merchantid)
    elif choice == 'W':
        return RequestsRecievedAndPending(mysql, merchantid)
    elif choice == 'R':
        return RequestsReceivedAndRejected(mysql, merchantid)
    elif choice == 'E':
        res = list(RequestsRecievedAndPending(mysql, merchantid))
        res.extend(RequestsReceivedAndAccepted(mysql, merchantid))
        res.extend(RequestsReceivedAndRejected(mysql, merchantid))
        return res


##  BUYER SIDE  ##
def PostedAndPending(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identification number for the buyer
    :return: a list of requirements posted by buyer and no supplier merchant has approved
    """
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement where MerchantID = '%s' and Requirement.Status='Post';", (merchantid,))
    requirements_posted = cur.fetchall()
    if not requirements_posted:
        message = 'No requirements were posted by you'
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
            # if no one accepted, then it is in pending state
            if not x:
                data_res.append(res)
        for i in range(len(data_res)):
            data_res[i]['Status'] = 'Pending'
        return data_res


def PostedAndAcceptedBySupplier(mysql, merchantid):
    """
    :param mysql: database connection object
    :param merchantid: unique merchant identification number for the buyer
    :return: a list of approved requirements posted by buyer along with information and ratings
    of merchant who has approved buyer requirements
    """
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement where MerchantID = '%s' and Requirement.Status='Post';", (merchantid,))
    requirements_posted = cur.fetchall()
    if not requirements_posted:
        message = 'No requirements were posted by you'
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
                    j['rating'] = SearchRatings(mysql, j['MerchantID'])
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
        delivered[i]['Status'] = 'Done'
    return delivered


def getBuyerRequests(mysql, merchantid, choice='R'):
    merchantid = int(merchantid)
    if choice == 'R':
        return PostedAndPending(mysql, merchantid)
    elif choice == 'A':
        return PostedAndAcceptedBySupplier(mysql, merchantid)
    elif choice == 'D':
        return PostedAndDone(mysql, merchantid)
    elif choice == 'E':
        res = []
        a = PostedAndPending(mysql, merchantid)
        b = PostedAndAcceptedBySupplier(mysql, merchantid)
        c = PostedAndDone(mysql, merchantid)
        if a:
            res.extend(a)
        if b:
            res.extend(b)
        if c:
            res.extend(c)
        return res


# SUPPLIER
def approveDeal(mysql, requirementID, productID):
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO RequirementAccepted values('{}','{}','{}')".format(requirementID, productID, "no"))
    except Exception as e:
        print("insert " + str(e))

    cur.execute(
        "UPDATE RequirementAccepted,Requirement SET RequirementAccepted.Status='{}'  WHERE RequirementAccepted.RequirementID='{}' AND Requirement.RequirementID='{}'".format(
            "yes", requirementID, requirementID, ))
    mysql.connection.commit()
    cur.execute(
        "UPDATE RequirementAccepted,Requirement SET RequirementAccepted.ProductID='{}'  WHERE RequirementAccepted.RequirementID='{}' AND Requirement.RequirementID='{}'".format(
            productID, requirementID, requirementID))
    mysql.connection.commit()


# BUYER
# ONLY AFTER PAYMENT
def acceptDeal(mysql, requirementID, merchantIDwhoPost, cartID):
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE Requirement,RequirementAccepted,Cart,Orders SET Requirement.Status= '{}' where Requirement.RequirementID='{}' and Orders.CartID='{}' and Requirement.MerchantID".format(
            "Done", requirementID, cartID, merchantIDwhoPost))

    mysql.connection.commit()


# SUPPLIER
def rejectDeal(mysql, requirementID):
    cur = mysql.connection.cursor()
    # cur.execute("UPDATE RequirementAccepted,Requirement SET RequirementAccepted.Status='{}' WHERE RequirementAccepted.RequirementID='{}' AND Requirement.RequirementID='{}'".format("no",requirementID,requirementID))
    try:
        cur.execute("INSERT INTO RequirementAccepted values('{}','{}','{}')".format(requirementID, "nothing", "no"))
    except Exception as e:
        print("insert " + str(e))
    mysql.connection.commit()


# SUPPLIER
def allProductID(mysql, merchantID):
    cur = mysql.connection.cursor()
    cur.execute("select * from Product where Sell='1' and MerchantID='{}'".format(merchantID))
    sellProduct = list(cur.fetchall())
    # print(sellProduct)
    return sellProduct


# BUYER
def deletePending(mysql, requirementID):
    cur = mysql.connection.cursor()
    cur.execute(
        "select * from RequirementAccepted where RequirementID='{}' and Status='{}'".format(requirementID, "yes"))
    a = cur.fetchall();
    loop = len(a)
    if (loop == 0):
        cur.execute("Delete from Requirement where RequirementID='{}'".format(requirementID))
        mysql.connection.commit()


def getInfo(mysql, requiremenID):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement where RequirementID='{}'".format(requiremenID))
    a = cur.fetchall()
    return a
