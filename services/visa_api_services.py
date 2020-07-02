import requests
import json
import os
import datetime


# cert=("/Users/sahanas/Desktop/Visa-Hackathon/services/cert.pem", '/Users/sahanas/Desktop/Visa-Hackathon/services/key_374cc983-558b-49dd-a55b-99d3cb3afac5.pem') #if you on MAC
cert=(os.path.abspath("services/cert.pem"),os.path.abspath("services/key_374cc983-558b-49dd-a55b-99d3cb3afac5.pem")) #if you on Windows
auth=("STT3WACAH2W19FH6H48A2117b1JIIYevI8qRcIQn2Zwhtdp4M", "81SYH42zc2CwJgtOzInj50e8zT6vr")
header={'Accept': 'application/json'}


def testConnection():
    url = "https://sandbox.api.visa.com/vdp/helloworld"
    r = requests.get(url, timeout=10,cert = cert,headers = {},auth = auth,data = {})
    print(r.text)


# B2B virtual payment methods
def CreateFundingAccount(funding_acc_no,buyerid,clientid='B2BWS_1_1_9999'):
    """
    :param funding_acc_no: PAN to register a funding account
    :param buyerid: buyer account number to identify proxy pool
    :param clientid: unique client identification to the VDP user
    :return: 0 if error and 1 if succesful
    creates a funding account for a buyerid
    """
    url = "https://sandbox.api.visa.com/vpa/v1/accountManagement/fundingAccount/create"
    p = json.loads(
        '''
    {
    "messageId": "2020-06-30T10:55:37.000Z",
    "clientId": "'''+clientid+'''",
    "buyerId": '''+buyerid+''',
    "accountNumber": '''+funding_acc_no+''',
    "currencyCode": "IND",
    "creditLimit": 10,
    "expirationDate": "2020-06-30T10:55:37.000Z"
    }
    ''')
    try:
        r = requests.post(url, timeout=10,
                      cert=cert,
                      headers=header,
                      auth=auth,
                      json=p)
        result = r.json()
        print(result)
        return 1
    except:
        print('error creating funding account')
        return 0


def CreateProxyPool(funding_acc_no,buyerid,pool_name,clientid='B2BWS_1_1_9999'):
    """
    :param funding_acc_no: PAN to register a funding account
    :param buyerid: buyer account number to identify proxy pool
    :param pool_name: unique pool identification number
    :param clientid: unique client identification to the VDP user
    :return: 0 if error and 1 if successful
    creates a proxy pool for a buyerid and attaches a funding account to it
    """
    url = "https://sandbox.api.visa.com/vpa/v1/proxy/CreateProxyPool"
    p = json.loads(
        '''{
            "messageId": "2020-06-30T11:11:13.000Z",
            "clientId": "'''+clientid+'''",
            "buyerId": "'''+buyerid+'''",
            "proxyAccountNumber": "'''+pool_name+'''",
            "proxyAccountType": "2",
            "proxyPoolType": "1",
            "authControlEnabled": true,
            "fundingAccountNumber":'''+funding_acc_no+''' ,
            "minAvailableAccounts": "3",
            "initialOrderCount": "5",
            "reOrderCount": "2"
            }''')
    try:
        r = requests.post(url, timeout=10,
                      cert=cert,
                      headers=header,
                      auth=auth,
                      json=p)
        result = r.json()
        print(result)
        return 1
    except:
        return 0


def createBuyer(mysql,buyerid,clientid="B2BWS_1_1_9999"):
    """
    :param mysql: database connection object
    :param buyerid: buyer account number to identify proxy pool
    :param clientid: unique client identification to the VDP user
    :return: created buyer using buyerid
    """
    cur = mysql.connection.cursor()
    cur.execute("select * from Merchant where MerchantID='"+buyerid+"';")
    mid,name,registeredName,email,contactNumber,address,password,mcc = cur.fetchone()
    cur.close()
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


def createBuyerAccount(mysql,buyerid,pool_id,clientid="B2BWS_1_1_9999"):
    """
    :param mysql: database connection object
    :param buyerid: buyer account number to identify proxy pool
    :param pool_id: unique pool identification number
    :param clientid: unique client identification to the VDP user
    :return: returns virtual account number using the pool_id and buyerid
    """
    url='https://sandbox.api.visa.com/vpa/v1/requisitionService'
    p= json.loads('''
        {
        "clientId": "'''+clientid+'''",
        "numberOfCards": "1",
        "messageId": "1526077012761",
        "action": "A",
        "buyerId": "'''+buyerid+'''",
        "proxyPoolId": "'''+pool_id+'''"
        }
    ''')
    r = requests.post(url, timeout=10,
                      cert=cert,
                      headers=header,
                      auth=auth,
                      json=p)
    result=r.json()
    account_number=result['accountNumber']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO B2BDetails (MerchantID, AccountNumber) VALUES (%s, %s);", (buyerid, account_number))
    mysql.connection.commit()
    return account_number


def createSupplier(mysql,virtual_acc_no,supplier_id,buyerid,clientid="B2BWS_1_1_9999"):
    """
    :param mysql: database connection object
    :param virtual_acc_no: virtual account number of supplier
    :param supplier_id: supplier id number to identify proxy pool
    :param buyerid: buyer account number to identify proxy pool
    :param clientid: unique client identification to the VDP user
    :return: returns 0 if a supplier account number could not be created and 1 if it was created
    """
    cur = mysql.connection.cursor()
    cur.execute("select * from Merchant where MerchantID='"+supplier_id+"';")
    mid, name, registeredName, email, contactNumber, address, password, mcc = cur.fetchone()
    cur.close()
    url = 'https://sandbox.api.visa.com/vpa/v1/supplier/CreateSupplier'
    p = json.loads(
        '''                        
        {
        "cardDetails": {
        "accountNumber": '''+virtual_acc_no+''',
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
    r = requests.post(url, timeout=10,cert=cert,headers=header,auth=auth, json=p)
    try:
        res=r.json()
        return 1
    except Exception as e:
        print('error creating supplier')
        print(e)
        print(r.text)
        return 0


def paymentProcessing(amount,buyerid,supplier_account_no ,clientid='B2BWS_1_1_9999'):
    """
    :param amount: amount to be deducted from virtual account
    :param buyerid: buyer account number to identify proxy pool
    :param supplier_account_no: supplier virtual account number
    :param clientid: unique client identification to the VDP user
    :return: returns 1 on succesful payment else 0
    uses buyerid and seller account number to transfer money
    """
    print(buyerid,supplier_account_no,amount)
    url = "https://sandbox.api.visa.com/vpa/v1/payment/ProcessPayments"
    a = amount
    p = json.loads(
        ''' 
    {
    "messageId": "2020-06-14T14:19:00.000Z",
    "clientId": "'''+clientid+'''",
    "buyerId": "'''+str(buyerid)+'''",
    "actionType": 1,
    "payment": {
    "accountNumber": "''' + str(supplier_account_no) + '''",
        "accountType": 2,
        "accountLimit": 100000,
        "paymentGrossAmount": ''' + str(a) + ''',
        "currencyCode": "INR",
        "paymentType": "CCC"
        }
        }
        ''')
    try:
        r = requests.post(url, timeout=10,
                          cert=cert,
                          headers=header,
                          auth=auth,
                          json=p)
        res=r.json()
        print(res)
        if res['statusDesc']:
            print(res['statusDesc'],' for rupees',amount )
        if res['statusDesc']=='Payment instruction completed successfully':
            return 1
        else:
            raise Exception
    except Exception as e:
        print("\nException when calling PaymentsApi->create_payment: %s\n" % e)
        return 0


def CheckB2BBalance(buyerid,supplier_account_no ,clientid='B2BWS_1_1_9999'):
    """
    :param buyerid: buyer account number to identify proxy pool
    :param supplier_account_no: supplier virtual account number
    :param clientid: unique client identification to the VDP user
    :return: returns account balance number
    """
    url = 'https://sandbox.api.visa.com/vpa/v1/accountManagement/fundingAccount/get'
    p = json.loads('''          
            {
            "messageId": "2020-06-29T04:44:19.000Z",
            "clientId": "'''+clientid+'''",
            "buyerId": '''+buyerid+''',
            "accountNumber": '''+supplier_account_no+'''
            }
        ''')
    r = requests.post(url, timeout=10,
                      cert=cert,
                      headers=header,
                      auth=auth,
                      json=p)
    result = r.json()
    return result


def register_merchant(mysql,mid,funding_acc_number):
    """
    :param mysql: database connection object
    :param mid: unique merchant identification number
    :param funding_acc_no: PAN to register a funding account
    complete B2B registration
    1. registers a funding account
    2. create proxy pool and link funding account
    3. create buyer and buyer virtual account
    4. create supplier and supplier virtual account
    """
    buyerid,supplier_id,pool_id = mid,mid,mid[:19]
    createBuyer(mysql,buyerid)
    #! problem with VDP API
        # CreateFundingAccount(funding_acc_number,buyerid)
        # CreateProxyPool(funding_acc_number,buyerid,pool_id)
    account_number = createBuyerAccount(mysql,buyerid,pool_id)
    createSupplier(mysql,account_number,supplier_id,buyerid)
    cur = mysql.connection.cursor()
    cur.execute("select * from PaymentType where MerchantID='"+mid+"';")
    result = cur.fetchone()
    if result!=None:
        cur.execute("update PaymentType set PayType='3' where MerchantID='"+mid+"';")
    else:
        cur.execute("INSERT INTO PaymentType (MerchantID, PayType) VALUES (%s, %s);", (mid, '2'))
    mysql.connection.commit()



# Merchant measurement API
def MerchantMeasurement(MCC = '5812'):
    """
    :param MCC: merchant category code as specified by Visa
    :return: performance indicators for the MCC using Merchant measurement API if no error or timeout
    """
    url = "https://sandbox.api.visa.com/merchantmeasurement/v1/merchantbenchmark"
    p = json.loads(
        '''  
            {
            "requestHeader": {
            "messageDateTime": "2020-06-29T06:17:04.327Z",
            "requestMessageId": "6da60e1b8b024532a2e0eacb1af58581"
            },
            "requestData": {
            "naicsCodeList": [
            ""
            ],
            "merchantCategoryCodeList": [
            "''' + MCC + '''"
            ],
            "merchantCategoryGroupsCodeList": [
            ""
            ],
            "postalCodeList": [
            ""
            ],
            "msaList": [
            "7362"
            ],
            "countrySubdivisionList": [
            ""
            ],
            "merchantCountry": "840",
            "monthList": [
            "201706"
            ],
            "accountFundingSourceList": [
            "ALl"
            ],
            "eciIndicatorList": [
            "All"
            ],
            "platformIDList": [
            "All"
            ],
            "posEntryModeList": [
            "All"
            ],
            "cardPresentIndicator": "All",
            "groupList": [
            "Standard"
            ]
            }
            } ''')
    try:
        r = requests.post(url,cert=cert,headers=header,auth=auth,json=p,timeout=10)
        res=r.json()
        data={}
        res = res['response']['responseData'][0]
        data['fraud_checked_sales_growth']=res['fraudChbktoSalesGrowthYoY']
        data['fraud_checked_to_Sales_Ratio']=res['fraudChbktoSalesRatio']
        data['non_fraud_checked_to_Sales_Ratio']=res['nonfraudChbktoSalesRatio']
        data['sales_transaction_growth_monthly']=res['salesTranCntGrowthMoM']
        data['sales_transaction_growth_yearly']=res['salesTranCntGrowthYoY']
        data['sales_volume_growth_monthly']=res['salesVolumeGrowthMoM']
        data['sales_volume_growth_yearly']=res['salesVolumeGrowthYoY']
        return data
    except:
        print('no data added for this code')
        return {}


# Merchant Locator API
def getMerchantsByMLOCAPI(merchantCategoryCode,radius,merchantID,latitude,longitude):
    """
    :param merchantCategoryCode: as identified by Visa
    :param radius: search radius in miles
    :param merchantID: Unique merchant identification number
    :param latitude, longitude: user coordinates
    :return: a list of merchants around the user location
    """
    if not radius:
        radius = '99'   
    url = "https://sandbox.api.visa.com/merchantlocator/v1/locator"
    now = datetime.datetime.now()
    messageDateTime = now.strftime("%Y-%m-%dT%H:%M:%S.000")
    p = json.loads(
        '''       
            {
            "header": {
                "messageDateTime": "'''+messageDateTime+'''",
                "requestMessageId": "'''+merchantID+'''",
                "startIndex": "0"
            },
            "searchAttrList": {
                "merchantCategoryCode": ["'''+merchantCategoryCode+'''"],
                "latitude": "'''+latitude+'''",
                "longitude": "'''+longitude+'''",
                "distance": "'''+radius+'''",
                "distanceUnit": "KM"
            },
            "responseAttrList": [
            "GNLOCATOR"
            ],
            "searchOptions": {
            "maxRecords": "10",
            "matchIndicators": "true",
            "matchScore": "true"
            }
            }
        ''')
    r = requests.post(url, timeout=100,cert=cert,headers=header,auth=auth,json=p)
    result = r.json()
    merchants = []
    result = result["merchantLocatorServiceResponse"]
    if(result["response"]):
        print("Merchants found")
        responses = result["response"]
        for response in responses:
            merchants.append(response["responseValues"])
    else:
        print("No Mechants found")
    return merchants


# Visa transaction control
def registerOnVTC(primaryAccountNumber):
    """
    :param primaryAccountNumber: PAN assosiated with user
    :return: registration document identifier
    """
    url = "https://sandbox.api.visa.com/vctc/customerrules/v1/consumertransactioncontrols"
    p = json.loads(
        '''
    {
    "primaryAccountNumber": "'''+ primaryAccountNumber +'''"
    }
        ''')
    r = requests.post(url, timeout=100,
                      cert=cert,
                      headers=header,
                      auth=auth,
                      json=p)
    result = r.json()
    if(result["resource"]):
        if(result["resource"]["documentID"]):
            return result["resource"]["documentID"]
    return None


def getAvailableMerchantControls(primaryAccountNumber):
    """
    :param primaryAccountNumber: PAN assosiated with user
    :return: returns available control rules
    """
    url = "https://sandbox.api.visa.com/vctc/customerrules/v1/merchanttypecontrols/cardinquiry"
    p = json.loads(
        '''
    {
    "primaryAccountNumber": "'''+ primaryAccountNumber +'''"
    }
    ''' )
    r = requests.post(url, timeout=100,
                        cert=cert,
                        headers=header,
                        auth=auth,
                        json=p)
    result = r.json()
    data = []
    if(result["resource"]):
        if(result["resource"]["availableMerchantTypeRules"]):
            for res in result["resource"]["availableMerchantTypeRules"]:
              data.append(res["name"])
            return data      

    return None


def getMerchantControlRules(documentID):
    """
    :param documentID: document identification number returned during registration
    :return: rules assosialted with the documentID
    """
    url = "https://sandbox.api.visa.com/vctc/customerrules/v1/consumertransactioncontrols/"+documentID+"/rules"
    p = json.loads(
        '''
            {}
        '''
    )
    r = requests.post(url, timeout=100,
                        cert=cert,
                        headers=header,
                        auth=auth,
                        json=p)
    result = r.json()
    data = []

    if(result["resource"]):
        result = result["resource"]
        for control in result["globalControls"]:
          data.append(control)
        for control in result["merchantControls"]:
          data.append(control)
        return data

    return None


def addMerchantControlRule(documentID,controlRule):
    """
    :param documentID: document identification number returned during registration
    :param controlRule: a dictionary containing either a global control or merchant control
    """
    url = "https://sandbox.api.visa.com/vctc/customerrules/v1/consumertransactioncontrols/"+documentID+"/rules"

    p = controlRule
    r = requests.post(url, timeout=100,
                        cert=cert,
                        headers=header,
                        auth=auth,
                        json=p)
    result = r.json()
    if(result["resource"]):
        return result["resource"]
    return None