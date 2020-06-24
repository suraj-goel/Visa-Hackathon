import requests
import json
import os

#cert=('./cert.pem','./key_374cc983-558b-49dd-a55b-99d3cb3afac5.pem')
cert=(os.path.abspath("services/cert.pem"),os.path.abspath("services/key_374cc983-558b-49dd-a55b-99d3cb3afac5.pem"))
auth=("STT3WACAH2W19FH6H48A2117b1JIIYevI8qRcIQn2Zwhtdp4M", "81SYH42zc2CwJgtOzInj50e8zT6vr")
header={'Accept': 'application/json'}

def testConnection():
    url = "https://sandbox.api.visa.com/vdp/helloworld"
    r = requests.get(url, timeout=10,
                 #put your certificate and key or just use mine
                  cert = cert,
                  headers = {},
                  auth = auth,
                  data = {})
    print(r.text)

#B2B virtual payment methods
def createSupplier(mysql,acc,supplier_id,buyerid='9210101012',clientid="B2BWS_1_1_9999"):
    # supplier id is Identifier used by the buyer to identify the supplier. This has to be unique for a buyer. It cannot contain spaces.
    #fetch buyer id from db corresponding to merchantid and set a new supplier id with account number for payment
    cur = mysql.connection.cursor()
    cur.execute("select * from Merchant where MerchantID='"+supplier_id+"';")
    mid, name, registeredName, email, contactNumber, address, password = cur.fetchone()
    cur.close()
    url = 'https://sandbox.api.visa.com/vpa/v1/supplier/CreateSupplier'
    p = json.loads(
        '''                        
        {
        "cardDetails": {
        "accountNumber": '''+acc+''',
        "accountType": "1",
        "actionType": "1"
        },
        "paymentExpirationDays": "10",
        "reminderNotificationDays": "9",
        "invoiceAttachmentRequired": "Y",
        "reminderNotificationRequired": "Y",
        "securityCodeRequired": "Y",
        "paymentControlRequired": "Y",
        "supplierDate": "MMDDYYYY",
        "enablePin": "",
        "supplierGLCode": "12345",
        "defaultCurrencyCode": "INR",
        "supplierLanguage": "en_US",
        "supplierCountryCode": "IND",
        "supplierPostalCode": "94404",
        "supplierState": "CA",
        "supplierCity": "FC",
        "supplierAddressLine1": "'''+address+'''",
        "supplierType": "VPA",
        "supplierName": "'''+registeredName+'''",
        "supplierId": "'''+supplier_id+'''",
        "buyerId": "'''+buyerid+'''",
        "clientId": "'''+clientid+'''",
        "messageId": "1525731018854"
        }
                ''')
    r = requests.post(url, timeout=10,
                      cert=cert,
                      headers=header,
                      auth=auth,
                      json=p)
    try:
        res=r.json()
        print(res['statusDesc'])
        return 1
    except Exception as e:
        print(e)
        print(r.text)
        print('error creating supplier')
        return 0

def createBuyerAccount(mysql,buyerid,clientid="B2BWS_1_1_9999"):
    url='https://sandbox.api.visa.com/vpa/v1/requisitionService'
    p= json.loads('''
        {
        "clientId": "'''+clientid+'''",
        "numberOfCards": "1",
        "messageId": "1526077012761",
        "action": "A",
        "buyerId": '''+buyerid+'''
        }
    ''')
    r = requests.post(url, timeout=10,
                      cert=cert,
                      headers=header,
                      auth=auth,
                      json=p)
    result=r.json()
    account_number=result['accountNumber']
    print('Account number set up for buyer')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO B2BDetails (MerchantID, AccountNumber) VALUES (%s, %s);", (buyerid, account_number))
    mysql.connection.commit()
    return account_number


def createBuyer(mysql,buyerid,clientid="B2BWS_1_Region_Bank_19401"):
    # client id is supplied by visa to identify the finantial institutaion that is offering this service(ignore it)
    cur = mysql.connection.cursor()
    cur.execute("select * from Merchant where MerchantID='"+buyerid+"';")
    mid,name,registeredName,email,contactNumber,address,password = cur.fetchone()
    cur.close()
    #The Company ID must be the same Company ID at the processor
    url='https://sandbox.api.visa.com/vpa/v1/buyerManagement/buyer/create'
    p = json.loads(
        '''  
            {
            "clientId":"'''+clientid+'''",
            "messageId": "1579589087445", 
            "contactInfo": {
            "addressLine1": "'''+address+'''",
            "addressLine2": "",
            "addressLine3": "",
            "buyerId": "'''+buyerid+'''",
            "buyerName": "TestPaymentFileLijie14",
            "city": "Austin",
            "companyId": "'''+mid+'''",
            "contactName": "'''+registeredName+'''",
            "countryCode": "IND",
            "defaultCurrencyCode": "INR",
            "emailAddress": "'''+email+'''",
            "phone1": "'''+contactNumber+'''",
            "phone2": "",
            "phone3": "",
            "phoneExt1": "",
            "phoneExt2": "",
            "phoneExt3": "",
            "state": "TX",
            "zipCode": "78759"
            }
            }
            ''')
    r = requests.post(url, timeout=10,
                      cert=cert,
                      headers=header,
                      auth=auth,
                      json=p)
    if r.json()['responseStatus']['status']=='success':
        print("buyer was created")


def paymentProcessing(amount,buyerid,supplier_account_no ,clientid='B2BWS_1_1_9999'):
    #fetch buyerid from database and supplier accunt number too
    url = "https://sandbox.api.visa.com/vpa/v1/payment/ProcessPayments"
    a = amount
    p = json.loads(
        ''' 
    {
    "messageId": "2020-06-14T14:19:00.000Z",
    "clientId": "'''+clientid+'''",
    "buyerId": '''+buyerid+''',
    "actionType": 1,
    "payment": {
    "accountNumber": ''' + supplier_account_no + ''',
        "accountType": 2,
        "accountLimit": 100,
        "paymentGrossAmount": ''' + str(a) + ''',
        "currencyCode": "INR",
        "paymentType": "CCC"
        }
        }
        ''')
    r = requests.post(url, timeout=10,
                      cert=cert,
                      headers=header,
                      auth=auth,
                      json=p)
    res=r.json()
    if res['statusDesc']:
        print(res['statusDesc'],' for rupees',amount )


def register_merchant(mysql,mid):
    #first we need to create a buyer profile for the merchant for which we need any unique number called buyerid
    buyerid,supplier_id = mid,mid
    createBuyer(mysql,buyerid)
    #we need to set up account number for buyer.. once buyer is created, the account number can be assigned and returned using this call
    account_number = createBuyerAccount(mysql,buyerid)
    #we can then use this account number to create his supplier profile
    createSupplier(mysql,account_number,supplier_id)
    #payment needs supplier account number and buyerid
    cur = mysql.connection.cursor()
    cur.execute("select * from PaymentType where MerchantID='"+mid+"';")
    result = cur.fetchone()
    if result!=None:
        cur.execute("update PaymentType set PayType='3' where MerchantID='"+mid+"';")
    else:
        cur.execute("INSERT INTO PaymentType (MerchantID, PayType) VALUES (%s, %s);", (mid, '2'))
    mysql.connection.commit()

#acc=register_merchant(mysql,"12324","APISupp-102")

#payment
#payment_amount=1200
#paymentProcessing(payment_amount,"12324",acc)