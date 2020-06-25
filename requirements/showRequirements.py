##   SUPPLIER SIDE    ##
# Received request posted by others
# proposal button can be added here and then we can add to RequirementAccepted database
# proposal accepts productid of only those that are sold by him
def RequestsReceived(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement where MerchantID <> '%s' and Status='Post';", (merchantid,))
    posts = cur.fetchall()
    return posts


# Accepted request posted by others accepted by you
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
                "Requirement.Status='Approved';",(merchantid,))
    rejected=cur.fetchall()
    return rejected


def RequestsRecievedAndPending(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Product where Product.ProductID=RequirementAccepted.ProductID "
                "and Requirement.RequirementID=RequirementAccepted.RequirementID and Product.MerchantID='%s' and "
                "Requirement.Status='Post';", (merchantid,))
    pending = cur.fetchall()
    return pending


##  BUYER SIDE  ##
# Status of request posted by you
# here i am showing history as well....we can remove it and add in order history or keep in both
# can create new filter for status as well
def RequestedPostedAndPending(mysql, merchantid):
    res = []
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement where MerchantID = '%s' ;", (merchantid,))
    requirements_posted = cur.fetchall()
    if not requirements_posted:
        message = 'No requirements were posted by you'
    else:
        data_res = []
        for i in requirements_posted:
            res = requirements_posted
            # retreive all accepts in case the requirement is still under post
            cur.execute(
                "select * from Requirement,RequirementAccepted,Merchant,Product where  Requirement.MerchantID = %s and Requirement.RequirementID='%s' and Requirement.RequirementID=RequirementAccepted.RequirementID and Merchant.MerchantID=Product.MerchantID and Product.ProductID=RequirementAccepted.ProductID and RequirementAccepted.Status='no' and Requirement.Status='Post';",
                (merchantid, i['RequirementID']))
            x = cur.fetchall()
            # if no one accepted, dont add accept list to disctonary
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
def RequestPostedAndPaid(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Merchant,Product where "
                "Requirement.RequirementID=RequirementAccepted.RequirementID and Merchant.MerchantID=Product.MerchantID "
                "and Product.ProductID=RequirementAccepted.ProductID and RequirementAccepted.Status='yes' and "
                "Requirement.Status='Approved' and Requirement.MerchantID='%s';", (merchantid,))
    out_for_delivery = cur.fetchall()
    return out_for_delivery


def RequestPostedAndDelivered(mysql, merchantid):
    cur = mysql.connection.cursor()
    cur.execute("select * from Requirement,RequirementAccepted,Merchant,Product where "
                "Requirement.RequirementID=RequirementAccepted.RequirementID and Merchant.MerchantID=Product.MerchantID "
                "and Product.ProductID=RequirementAccepted.ProductID and RequirementAccepted.Status='yes' and "
                "Requirement.Status='Delivered' and Requirement.MerchantID='%s';", (merchantid,))
    delivered = cur.fetchall()
    return delivered
