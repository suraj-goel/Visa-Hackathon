from functools import wraps
from datetime import datetime
import jinja2
import os
from datetime import timedelta
from flask import *
from flask import session
from services.db.db_connection import set_connection
from search_merchants.searchMerchant import getCurrentLocation
from place_order.displayProduct import displayAllProducts, displayAllOffers
from search_merchants.searchProducts import getSearchResults
from login_registration.registerMerchant import checkIfExistingMerchant, registerNewMerchant, checkPayType, insertLocation, updateLocation
from login_registration.addressconversion import getCoordinates
from accounts.validate_accounts import validation
from place_order.displayCart import addToCart, getMerchantInfo
from manage_inventory.SearchInventory import *
from manage_inventory.addProduct import addNewProduct, getCategories
from manage_inventory.updateProduct import *
from orders_management.orderHistory import getOrders
from requirements.requirements import *
from services.visa_api_services import register_merchant, paymentProcessing
from services.visa_api_services import getMerchantsByMLOCAPI
from services.cybersourcePayment import simple_authorizationinternet
from requirements.showRequirements import *
from negotiation.negotiation import *
from payment.confirmPayment import *
from manage_inventory.supplierupdater import *
from manage_offers.displayOffers import *
from orders_management.orderHistory import Delivered, AddRating
import requests
from delivery_management.delivery import getDelivery,YourRatings
from search_merchants.searchMerchantCategory import *
from merchant_performance.merchant_performance import getPerformanceStats
from services.visa_api_services import registerOnVTC,getAvailableMerchantControls,getMerchantControlRules,addMerchantControlRule


# set up controller, session configurations and maps configurations
app = Flask(__name__, static_folder='')
app.jinja_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader(['.'])])
app.config['GOOGLEMAPS_KEY'] = ""
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=300)
mysql = set_connection(app)
geocode_api_key = 'AIzaSyAntxrxhQu11TxFD9wEe7JxxW1UZ0HQXR'
geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'


## LOGIN AND REGISTRATION ##
# auth decorator to make sure user logs in before accessing contents of website
def login_required(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        if 'merchantID' in session:
            id = session['merchantID']
            if request.path == '/register/' or request.path == '/login/':
                return redirect('/search')
            else:
                if 'pay_type' in session:
                    return function_to_protect(*args, **kwargs)
                else:
                    c = checkPayType(mysql, id)
                    if c==True:
                        session.permanent = True
                        session['pay_type'] = True
                        return function_to_protect(*args, **kwargs)
                    elif request.path == '/registerCyber/':
                        return function_to_protect(*args, **kwargs)
                    else:
                        return redirect(url_for('registerCyber'))
        elif request.path == '/register/' or request.path == '/login/':
            return function_to_protect(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper


@app.route('/login/', methods=['GET', 'POST'])
@login_required
def login():
    if request.method == 'POST':
        session.pop('merchantID', None)
        email = request.form.get('email')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("select * from Merchant where EmailID='{}' and Password='{}';".format(email, password))
        users = cur.fetchone()
        cur.close()
        if users is not None:
            session.permanent = True
            session['merchantID'] = users['MerchantID']
            return redirect(url_for('showAll'))
        else:
            flash('Incorrect Email and Password combination')
            return redirect(url_for('login'))
    return render_template("./login_registration/login.html")


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register/', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        merchantName = request.form.get('merchant_name')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirm_password')
        address = request.form.get('address')
        contactNumber = request.form.get('contact_number')
        registeredName = request.form.get('registered_name')

        if password != confirmPassword:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        if checkIfExistingMerchant(mysql,email):
            flash('Email already registered')
            return redirect(url_for('register'))
        else:
            try:
                geocode_res = getCoordinates(address)
                if len(geocode_res) == 0:
                    flash('Enter Valid Location')
                    return redirect(url_for('register'))
                latlong = geocode_res[0]['geometry']['location']
            except requests.exceptions.RequestException as e:
                flash('Enter Valid Location')
                return redirect(url_for('register'))

            session.permanent = True
            id = registerNewMerchant(mysql, email, password, merchantName, address, contactNumber, registeredName)
            insertLocation(mysql, latlong['lat'], latlong['lng'], id)
            session['merchantID'] = id
            return redirect(url_for('registerCyber'))
    return render_template("./login_registration/register1.html")


## SEARCH MERCHANTS, PRODUCTS AND CATEGORY ##
@app.route('/', methods=['POST', 'GET'])
@app.route('/search', methods=['POST', 'GET'])
@login_required
def showAll():
    currentMerchantID =  session['merchantID']
    currentLocation = getCurrentLocation(mysql, currentMerchantID)
    if request.method == "POST":
        search_option = request.form['search']
        filter = request.form.get('offerbox')
        radius = request.form['radius']
        product = request.form['name']
        data = getSearchResults(mysql, currentMerchantID, product, search_option, filter, radius)
        return render_template('./search_merchants/search.html', data=data, currentLocation=currentLocation,
                               search_option=search_option)
    data = getSearchResults(mysql, currentMerchantID)
    return render_template("./search_merchants/search.html", currentLocation=currentLocation, data=data)


@app.route('/searchbycategory',methods=['POST', 'GET'])
@login_required
def searchbycategory():
    currentMerchantID = session['merchantID']
    currentLocation = getCurrentLocation(mysql, currentMerchantID)
    data=[]
    if request.method == "POST":
        data=[]
        category = request.form["name"]
        radius = str(request.form['radius'])
        categorycode = getMerchantCategoryCode(mysql,category)
        if(len(categorycode)):
            code = str(categorycode[0]['Code'])
            try:
                data = getMerchantsByMLOCAPI(code,radius,currentMerchantID,currentLocation['Latitude'],currentLocation['Longitude'])
            except Exception as e:
                print(e)
    return render_template('./search_merchants/searchbycategory.html',data=data,currentLocation=currentLocation)


## ORDER PLACEMENT AND CART MANAGEMENT ##
Check = False
def modify():
    global Check
    Check = True


@app.route('/merchant/<merchant_id>', methods=['GET', 'POST'])
@login_required
def showPlaceOrder(merchant_id):
    if request.method == 'GET':
        currentSelectedMerchantID = merchant_id
        session['mid'] = currentSelectedMerchantID
        products = displayAllProducts(mysql, currentSelectedMerchantID)
        offers = displayAllOffers(mysql, currentSelectedMerchantID)
        return render_template("./place_order/place_order.html", products=products, offers=offers, len=len(products),
                               merchantID=merchant_id)
    else:
        session['qty'] = request.form.getlist("qty[]")
        session['ProductID'] = request.form.getlist("ProductID[]")
        session['Name'] = request.form.getlist("Name[]")
        session['Description'] = request.form.getlist("Description[]")
        session['Price'] = request.form.getlist("Price[]")
        session['offers'] = request.form.getlist("offers[]")
        session['discountPrice'] = request.form.getlist("discountPrice[]")
        session['type'] = 'simple'
        return redirect(url_for('showCart', merchant_id=merchant_id))


@app.route("/merchant/<merchant_id>/cart", methods=['GET', 'POST'])
@login_required
def showCart(merchant_id):
    totalQuantity = 0
    seller_id = merchant_id
    session['mid'] = seller_id
    qty = []
    ProductID = []
    Name = []
    Description = []
    Price = []
    Offers = []
    discountPrice = []
    emailID = ""
    contact = ""
    type = session['type']
    totalCost = 0
    totalDiscountCost = 0
    loggmerchant_id = session['merchantID']
    session['merchantID'] = loggmerchant_id
    if request.method == 'GET':
        try:
            if type == 'simple':
                qty = session['qty']
                ProductID = session['ProductID']
                Name = session['Name']
                Description = session['Description']
                Price = session['Price']
                Offers = session['offers']
                discountPrice = session['discountPrice']
                data = getMerchantInfo(mysql, seller_id)
                emailID = data[0]
                contact = data[1]
                pf = '1'
                session['payment_flag'] = pf
                l = len(qty)
                for i in range(0, l):
                    totalQuantity += int(qty[i])
                    totalCost += (int)(Price[i]) * (int)(qty[i])
                    totalDiscountCost += (int)(discountPrice[i])
            elif type == 'request':
                qty = session['qty']
                ProductID = session['ProductID']
                Name = session['Name']
                Description = session['Description']
                Price = session['Price']
                discountPrice = session['discountPrice']
                data = getMerchantInfo(mysql, seller_id)
                emailID = data[0]
                contact = data[1]
                pf = '2'
                session['payment_flag'] = pf
                l = len(qty)

                for i in range(0, l):
                    totalQuantity += int(qty[i])
                    totalCost += (int)(Price[i])
                    totalDiscountCost += (int)(discountPrice[i])
            elif type == 'negotiate':
                qty = session['qty']
                ProductID = session['ProductID']
                Name = session['Name']
                Description = session['Description']
                totalCost = session['totalCost']
                seller_id = session['mid']
                data = getMerchantInfo(mysql, seller_id)
                emailID = data[0]
                contact = data[1]
                pf = '3'
                session['payment_flag'] = pf
                totalDiscountCost = session['finalPriceChange']
                l = len(qty)
                for i in range(0, l):
                    totalQuantity += int(qty[i])
        except Exception as e:
            print("exception details " + str(e))
        return render_template("./place_order/cart.html", merchantID=merchant_id, qty=qty, ProductID=ProductID,
                               Name=Name, Description=Description, Price=Price, Offers=Offers,
                               discountPrice=discountPrice, len=len(qty), totalQuantity=totalQuantity, emailID=emailID,
                               contact=contact, type=type, totalDiscountCost=totalDiscountCost, totalCost=totalCost)
    else:
        ProductID = request.form.getlist("ProductId[]")
        qty = request.form.getlist("qty[]")
        Name = request.form.getlist("Name[]")
        Description = request.form.getlist("Description[]")
        Price = request.form.getlist("discountPrice[]")
        Type = request.form.get("type")
        finalPrice = request.form.get('finalPrice')
        finalDiscountPrice = request.form.get('finalDiscountPrice')
        NegotitatedRequestAmount = request.form.get('NegotiatedRequestAmount')
        status = 'N'
        if (Type == 'Process Payment'):
            status = 'P'
        addToCart(mysql, qty, ProductID, Name, Description, Price, loggmerchant_id, status, finalPrice,
                  finalDiscountPrice, NegotitatedRequestAmount)
        session['qty'] = []
        session['ProductID'] = []
        session['type'] = type
        session['mid'] = seller_id
        session['merchantID'] = loggmerchant_id
        session['finalDiscountPrice'] = finalDiscountPrice
        session['fqty'] = qty
        session['fProductID'] = ProductID
        if (Type == 'Process Payment'):
            amount = finalDiscountPrice
            return render_template('./payment/payment.html', amount=amount)
        else:
            return redirect(url_for('negotiation'))


## INVENTORY MANAGEMENT ##
@app.route('/inventory/', methods=['POST', 'GET'])
@login_required
def inventory():
    merchantid = session['merchantID']
    c = getCategories(mysql)
    try:
        message = session['message_product_add']
        session['message_product_add'] = None
    except:
        message = None
    if request.method == 'POST':
        filter = request.form['filter']
        items = getAllProducts(mysql, merchantid, filter)
        return render_template("./manage_inventory/inventory.html", items=items, filter=filter, category=c,
                               message=message)
    else:
        items = getAllProducts(mysql, merchantid, "S")
        return render_template("./manage_inventory/inventory.html", items=items, filter='S', category=c,
                               message=message)


@app.route('/addproduct', methods=['POST', 'GET'])
@login_required
def addproduct():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        category = request.form.get('category')
        if category == 'others':
            category = request.form['other_category']
        sell = request.form['sell']
        merchantID = session['merchantID']
        message = addNewProduct(name, description, price, quantity, category, sell, merchantID, mysql)
        session['message_product_add'] = message
    return redirect(url_for('inventory'))


@app.route('/inventory/edit/<productID>', methods=['POST', 'GET'])
@login_required
def editProduct(productID):
    productID = productID
    categories = getCategories(mysql)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        category = request.form.get('category')
        if category == 'others':
            category = request.form['other_category']
        sell = request.form['sell']
        merchantID =  session['merchantID']
        message = updateProduct(productID, merchantID, mysql, name, description, price, quantity, category, sell)
        session['message_product_add'] = message
        return redirect(url_for('inventory'))
    else:
        cur = mysql.connection.cursor()
        query = "SELECT * FROM Product WHERE ProductID = '{}'".format(productID)
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return render_template("./manage_inventory/editProduct.html", data=data[0], category=categories, productID=productID)


## DELIVERY MANAGEMENT ##
@app.route('/delivered', methods=['POST'])
@login_required
def delivered():
    merchantid= session['merchantID']
    orderid=request.form['orderid']
    Delivered(mysql,orderid,merchantid)
    return redirect(url_for('orders'))


@app.route('/rating',methods=['POST','GET'])
@login_required
def ratings():
    rating= request.form['rating']
    order=request.form['orderidrated']
    AddRating(mysql,order,rating)
    return redirect(url_for('orders'))


@app.route('/delivery_management', methods=['GET', 'POST'])
@login_required
def delivery_management():
    merchantid = session['merchantID']
    delivered_filter = 'yes'
    if request.method == 'POST':
        delivered_filter = request.form['filter']
    delivery = getDelivery(mysql, merchantid, delivered_filter)
    avg_ratings=YourRatings(mysql,merchantid)
    return render_template('./delivery_management/delivery_management.html',history=delivery,avg_ratings=avg_ratings,filter=delivered_filter)


## ORDERS MANAGEMENT ##
@app.route('/orders', methods=['POST', 'GET'])
@login_required
def orders():
    merchantid =  session['merchantID']
    delivered_filter = 'yes'
    if request.method == 'POST':
            delivered_filter = request.form['filter']
    history = getOrders(mysql, merchantid, delivered_filter)
    return render_template('./orders_management/order_management.html', history=history, filter=delivered_filter)


## MERCHANR PERFORMANCE ##
@app.route('/performance', methods=['POST', 'GET'])
@login_required
def performance():
    merchantid=session["merchantID"]
    data=getPerformanceStats(mysql,merchantid)
    return render_template('./merchant_performance/merchant_performance.html',data=data)


## ACCOUNT MANAGEMENT ##
@app.route('/accounts/', methods=['GET', 'POST'])
@login_required
def displayaccountsdetails():
    merchant_id = session['merchantID']
    cur = mysql.connection.cursor()
    cur.execute("select * from Merchant where MerchantID='" + merchant_id + "';")
    result = cur.fetchone()
    cur.close()
    return render_template("./accounts/displayAccountDetails.html", result=result)


@app.route('/editaccountinfo/', methods=['GET', 'POST'])
@login_required
def editAccountDetails():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        merchant_id = session['merchantID']  # session['MerchantID']
        name = request.form['name']
        registeredName = request.form['registeredName']
        email = request.form['emailid']
        contactno = request.form['contactno']
        address = request.form['address']
        password = request.form['password']
        r = validation(mysql, merchant_id, name, registeredName, email, contactno, address, password)
        if r[2] == 0:
            if "'" in address:
                a, c = address.split("'")
                address = a+chr(39)+c
            if "'" in registeredName:
                a, c = registeredName.split("'")
                registeredName = a+chr(39)+c

            if "'" in password:
                a, c = password.split("'")
                password = a+chr(39)+c
            try:
                geocode_res = getCoordinates(address)
                if len(geocode_res) == 0:
                    flash('Enter Valid Location')
                    result = r[0]
                    return render_template("./accounts/editAccountDetails.html", result=result)
                latlong = geocode_res[0]['geometry']['location']
            except requests.exceptions.RequestException as e:
                flash('Enter Valid Location')
                result = r[0]
                return render_template("./accounts/editAccountDetails.html", result=result)
            updateLocation(mysql, latlong['lat'], latlong['lng'], merchant_id)
            cur.execute(f"""update Merchant set Name = "{name}", RegisteredName = "{registeredName}", EmailID = "{email}", ContactNumber = "{contactno}", Address = "{address}", password = "{password}" where MerchantID="{merchant_id}";""")
            mysql.connection.commit()
            return redirect('/accounts/')
        else:
            result = r[0]
            if (r[1][0]):
                flash("Name already exists, please enter a new one.")
            if (r[1][1]):
                flash("Registered Name already exists, please enter a new one.")
            if (r[1][2]):
                flash("Email already exists, please enter a new one.")
            if (r[1][3]):
                flash("Contact Number already exists, please enter a new one.")
            if (r[1][4]):
                flash("Address already exists, please enter a new one.")
            return render_template("./accounts/editAccountDetails.html", result=result)
    merchant_id =session['merchantID']
    cur.execute("select * from Merchant where MerchantID='{}'".format(merchant_id))
    result = cur.fetchone()
    cur.close()
    return render_template("./accounts/editAccountDetails.html", result=result)



## PAYMENT MANAGEMENT ##
@app.route('/registerCyber/', methods=['GET', 'POST'])
def registerCyber():
    if 'merchantID' not in session:
        return redirect(url_for('login'))
    merchant_id = session['merchantID']
    cur = mysql.connection.cursor()
    cur.execute("select * from CybersourceMerchant where MerchantID='{}';".format(merchant_id))
    result = cur.fetchone()
    if 'pay_type' in session:
        b2b = True
    else:
        b2b = False
    if request.method == 'POST':
        name = request.form['name']
        aggregatorID = request.form['aggregatorid']
        cardAcceptorID = request.form['cardacceptorid']
        if b2b == False:
            funding_acc_number = request.form['funding_acc_number']
        if result == None:
            cur.execute("insert into CybersourceMerchant(AggregatorID,CardAcceptorID,Name,MerchantID) values (%s,%s,%s,%s);",(aggregatorID, cardAcceptorID, name, merchant_id))
            cur.execute("select * from PaymentType where MerchantID='{}';".format(merchant_id))
            r = cur.fetchone()
            if r == None:
                cur.execute("INSERT INTO PaymentType (MerchantID, PayType) VALUES (%s, %s);", (merchant_id, '1'))
                register_merchant(mysql, merchant_id, funding_acc_number)
            else:
                cur.execute("update PaymentType set PayType='3' where MerchantID='{}';".format(merchant_id))
            mysql.connection.commit()
        else:
            cur.execute("update CybersourceMerchant set Name = '" + name + "', AggregatorID = '" + aggregatorID + "', CardAcceptorID = '" + cardAcceptorID + "' where MerchantID='" + merchant_id + "';")
        mysql.connection.commit()
        return redirect(url_for('showAll'))
    return render_template("./accounts/cyberSourceDetails.html", result=result, b2b=b2b)


@app.route('/payments/', methods=['GET', 'POST'])
@login_required
def payment():
    amount = 0
    try:
        amount = request.form['finalDiscountPrice']
    except Exception as e:
        print("payment" + str(e))
    return render_template("./payment/payment.html", amount=amount)


@app.route('/cybersource/', methods=['GET', 'POST'])
@login_required
def cybersource():
    qty=session['fqty']
    ProductID=session['fProductID']
    sellerId = session['mid'] # why?
    merchant_id = session['merchantID']
    cur = mysql.connection.cursor()
    cur.execute("select AggregatorID,CardAcceptorID,Name from CybersourceMerchant where MerchantID='"+sellerId+"';")
    result = cur.fetchone()
    aggregatorID,cardAcceptorID,name = result['AggregatorID'],result['CardAcceptorID'],result['Name']
    if request.method == 'POST':
        amount = request.form.getlist('amount')[0]
        username = request.form.getlist('username')[0]
        cardNumber = request.form.getlist('cardNumber')[0]
        month = request.form.getlist('month')[0]
        year = request.form.getlist('year')[0]
        cvv = request.form.getlist('CVV')[0]
        status = simple_authorizationinternet(cardNumber,month,year,amount,aggregatorID,cardAcceptorID,username)
        if (status == 1):
            if (session['payment_flag'] == '1'):
                addToOrders(mysql, qty, ProductID, merchant_id, amount, datetime.today().strftime('%Y-%m-%d'))
            elif (session['payment_flag'] == '2'):
                addToOrders(mysql, qty, ProductID, merchant_id, amount, datetime.today().strftime('%Y-%m-%d'),session['payment_flag'], session['requirementid'])
            else:
                addToOrders(mysql, qty, ProductID, merchant_id, amount, datetime.today().strftime('%Y-%m-%d'),session['payment_flag'], session['negotiationID'])
            updateSupplierInventory(mysql, ProductID,qty)
            return redirect(url_for('showAll'))
        else:
            flash("Some details were invalid, please enter the correct values.")
    return render_template("./payment/payment.html",amount=amount)


@app.route('/b2bpay/', methods=['GET','POST'])
@login_required
def b2bpay():
    merchant_id = session['merchantID']
    qty = session['fqty']
    ProductID = session['fProductID']
    sellerId = session['mid']
    cur = mysql.connection.cursor()
    cur.execute("select AccountNumber from B2BDetails where MerchantID='"+sellerId+"';")
    accountNumber = cur.fetchone()['AccountNumber']
    if request.method == 'POST':
        amount = request.form.getlist('amount')[0]
        status = paymentProcessing(amount, merchant_id, accountNumber)
        if (status == 1):
            if (session['payment_flag'] == '1'):
                addToOrders(mysql, qty, ProductID, merchant_id, amount, datetime.today().strftime('%Y-%m-%d'))
            elif (session['payment_flag'] == '2'):
                addToOrders(mysql, qty, ProductID, merchant_id, amount, datetime.today().strftime('%Y-%m-%d'),session['payment_flag'], session['requirementid'])
            elif (session['payment_flag'] == '3'):
                addToOrders(mysql, qty, ProductID, merchant_id, amount, datetime.today().strftime('%Y-%m-%d'),session['payment_flag'], session['negotiationID'])
            updateSupplierInventory(mysql, ProductID,qty)
            return redirect(url_for('showAll'))
        else:
            flash("Error in payment, check account details again or try different payment")
    return render_template("./payment/payment.html",amount=amount)


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    qty=session['fqty']
    ProductID=session['fProductID']
    sellerId = session['mid'] # why?
    merchant_id = session['merchantID']
    amount  = session['finalDiscountPrice']
    cur = mysql.connection.cursor()
    status = 1
    if (status == 1):
        print('Payment Authorized')
        if (session['payment_flag'] == '1'):
            addToOrders(mysql, qty, ProductID, merchant_id, amount, datetime.today().strftime('%Y-%m-%d'))
        elif (session['payment_flag'] == '2'):
            addToOrders(mysql, qty, ProductID, merchant_id, amount, datetime.today().strftime('%Y-%m-%d'),session['payment_flag'], session['requirementid'])
        else:
            addToOrders(mysql, qty, ProductID, merchant_id, amount, datetime.today().strftime('%Y-%m-%d'),session['payment_flag'], session['negotiationID'])
        updateSupplierInventory(mysql, ProductID, qty)  # productID=ProductList
        return redirect(url_for('showAll'))
    else:
        print('Payment not authorized, please enter the correct details')
        flash("Some details were invalid, please enter the correct values.")
        # pass the correct values recieved from session (refer this for more info @app.route("/merchant/<merchant_id>/cart",methods=['GET','POST']))
    return render_template("./payment/payment.html",amount=amount)


## NEGOTIATION MANAGEMENT ##
@app.route('/negotiation',methods=['GET','POST'])
@login_required
def negotiation():
    choice = 'E'
    merchant_id = session['merchantID']
    gotList = displayAllNegotiation(mysql, merchant_id)
    productList = gotList[1]
    allNegotiation = gotList[0]
    contactInfo  = gotList[2]
    if (request.method == 'POST'):
        try:
            choice = request.form["filterbuyer"]
            if(choice!='E'):
                gotList = displayNegotiationType(mysql,merchant_id,choice)
                productList = gotList[1]
                allNegotiation = gotList[0]
                contactInfo = gotList[2]
                return render_template("./negotiation/negotiation.html", buy_items=allNegotiation,profile=2,buyer_choice=choice,productList=productList,sellInfo=contactInfo)
        except Exception as e:
            print("Nofiter"+str(e))
        try:
            Delete = request.form['Delete']
            negotiationID = request.form["negotiationID"]
            deleteNegotiation(mysql,negotiationID)
            return redirect(request.url)
        except Exception as e:
            print("noD"+str(e))
        try:
            session['type'] = 'negotiate'
            session['negotiationID'] = request.form['negotiationID']
            session['finalPriceChange'] = request.form['Amount2']
            session['qty'] = request.form.getlist('qty[]')
            session['Description'] = request.form.getlist('Description[]')
            session['ProductID'] = request.form.getlist('ProductID[]')
            session['Name']  = request.form.getlist('Name[]')
            seller_id = request.form['supplier']
            session['mid'] = seller_id
            session['totalCost'] = request.form['Amount1']
            return redirect(url_for('showCart',merchant_id=seller_id))
        except Exception as e:
            print("a2"+str(e))

        try:
            session['type'] = 'negotiate'
            session['negotiationID'] = request.form['negotiationID']
            session['finalPriceChange'] = request.form['Amount1']
            session['qty'] = request.form.getlist('qty[]')
            session['Description'] = request.form.getlist('Description[]')
            session['ProductID'] = request.form.getlist('ProductID[]')
            session['Name']  = request.form.getlist('Name[]')
            seller_id = request.form['supplier']
            session['mid'] = seller_id
            session['totalCost'] = request.form['Amount1']
            return redirect(url_for('showCart',merchant_id=seller_id))
        except Exception as e:
            print("a1"+str(e))
        return render_template("./negotiation/negotiation.html", buy_items=allNegotiation,profile=2,buyer_choice=choice,productList=productList,sellInfo = contactInfo)
    else:
        return render_template("./negotiation/negotiation.html",buy_items=allNegotiation,profile=2,buyer_choice=choice,productList=productList,sellInfo = contactInfo)

@app.route('/negotiationsupplier',methods=['GET','POST'])
@login_required
def negotiationsupplier():
    merchant_id = session['merchantID']
    groupList = showNegotiation(mysql, merchant_id)
    contactInfo = groupList[0]
    sellCart = groupList[1]
    Amount = groupList[2]
    loop = len(sellCart)
    if (request.method == 'POST'):
        try:
            negotiationID = request.form['negotiationID']
            NegAmount  = request.form['NegPrice']
            status = "accepted"
            updateNegotiation(mysql,negotiationID,status,NegAmount)
            groupList = showNegotiation(mysql, merchant_id)
            contactInfo = groupList[0]
            sellCart = groupList[1]
            Amount = groupList[2]
            return render_template("./negotiation/negotiation.html", sup_items=sellCart, profile=1,
                                   contactInfo=contactInfo, loop=loop, Amount=Amount)
        except Exception as e:
            print("apn"+str(e))

        try:
            Reject = request.form['Reject']
            negotiationID = request.form['negotiationID']
            NegAmount = request.form['NegPrice']
            print(negotiationID)
            status = "rejected"
            updateNegotiation(mysql,negotiationID,status,NegAmount)
            groupList = showNegotiation(mysql, merchant_id)
            contactInfo = groupList[0]
            sellCart = groupList[1]
            Amount = groupList[2]
            return render_template("./negotiation/negotiation.html", sup_items=sellCart, profile=1,
                                   contactInfo=contactInfo, loop=loop, Amount=Amount)
        except Exception as e:
            print("rn"+str(e))

        return render_template("./negotiation/negotiation.html",sup_items=sellCart,profile=1,contactInfo=contactInfo,loop=loop,Amount=Amount)
    else:
        return render_template("./negotiation/negotiation.html",sup_items=sellCart,profile=1,contactInfo=contactInfo,loop=loop,Amount=Amount)


## REQUIREMENT MANAGEMENT ##
@app.route('/requirements', methods=['GET', 'POST'])
@login_required
def requirements():
    merchant_id = session['merchantID']
    if (request.method == 'GET'):
        merchant_id = session['merchantID']# get from session
        registeredName = showBusinessName(mysql, merchant_id)
        return render_template("./requirements/requirements.html", registeredName=registeredName, profile=1)
    else:
        merchant_id = session['merchantID'] # get from session
        title = request.form.get('title')
        description = request.form.get('description')
        quantity = request.form.get('Quantity')
        price = request.form.get('ExpectPrice')
        print(price)
        status = "Post"
        saveRequirements(mysql, merchantID=merchant_id, title=title, description=description, quantity=quantity,
                         price=price, status=status)
        return redirect(url_for('showbuyerrequirements'))


@app.route('/search_requirement', methods=['POST'])
@login_required
def search_requirement():
    merchantid=session['merchantID']
    search=request.form['search_name']
    choice = 'P'
    items = getSupplierRequestsSearch(mysql, merchantid,search)
    sellProduct = allProductID(mysql,merchantid)
    return render_template('./requirements/requirements.html', sup_items=items, choice=choice, profile=2,sellProduct=sellProduct)


@app.route('/requirementssupplier', methods=['GET', 'POST'])
@login_required
def showsupplierrequirements():
    merchantid = session['merchantID']
    sellProduct = allProductID(mysql,merchantid)
    if request.method == 'POST':
        try:
            choice = request.form['filtersupplier']
            items = getSupplierRequests(mysql, merchantid, choice)
            print('$$', items)
            return render_template('./requirements/requirements.html', sup_items=items, choice=choice, profile=2,sellProduct=sellProduct)
        except Exception as e:
            print("filtersupplier" + str(e))
        try:
            requirementid = request.form['requirementID']
            productID = request.form['selectProduct']
            approveDeal(mysql,requirementid,productID)
            return redirect(request.url)
        except Exception as e:
            print("APPROVE" + str(e))
        return render_template(url_for('requirements'))
    else:
        choice = 'P'
        items = getSupplierRequests(mysql, merchantid, choice)
        return render_template('./requirements/requirements.html', sup_items=items, choice=choice, profile=2,sellProduct=sellProduct)


@app.route('/requirementsbuyer', methods=['GET', 'POST'])
@login_required
def showbuyerrequirements():
    merchantid = session['merchantID']
    if request.method == 'POST':
        try:
            choice = request.form['filterbuyer']
            items = getBuyerRequests(mysql, merchantid, choice)
            return render_template('./requirements/requirements.html', buy_items=items, buyer_choice=choice, profile=3)
        except Exception as e:
            print("filterbuyer" + str(e))
        try:
            requirementID = request.form['requirementID']
            deletePending(mysql,requirementID)
            return redirect(request.url)
        except Exception as e:
            print("NO NOT DELETE"+ str(e))
        try:
            session['type'] = 'request'
            session['requirement_payment']=True
            session['ProductID'] = request.form.getlist('ProductID[]')
            session['Name'] = request.form.getlist('Name[]')
            session['Description'] = request.form.getlist('Description[]')
            session['qty'] = request.form.getlist('qty[]')
            session['PriceItem'] = request.form.getlist('PriceItem[]')
            session['mid'] = request.form.get('merchantWhoAP')
            session['requirementid'] = request.form.get('requirementID')
            seller_id = session['mid']
            Price = []
            loop = len(session['PriceItem'])
            for i in range(0,loop):
                Price.append((str)((int)(session['PriceItem'][i])*(int)(session['qty'][i])))
            session['Price'] = Price
            session['discountPrice'] = Price
            return redirect(url_for('showCart',merchant_id=seller_id))
        except Exception as e:
            print("AC" + str(e))
        return render_template(url_for("requirements"))

    else:
        choice = 'E'
        items = getBuyerRequests(mysql, merchantid, choice)
    return render_template('./requirements/requirements.html', buy_items=items, buyer_choice=choice, profile=3)


## OFFER MANAGEMENT ##
@app.route('/offers',methods=['GET', 'POST'])
@login_required
def showoffers():
    merchantID = session['merchantID']
    data = displayOffersPage(mysql,merchantID)
    cur=mysql.connection.cursor()
    cur.execute("SELECT Name FROM Product WHERE MerchantID = '{}'".format(merchantID))
    try:
        message = session['message_offer_add']
        session['message_offer_add'] = None
    except:
        message = None
    product=[i['Name'] for i in list(cur.fetchall())]
    return render_template("./manage_offers/offers.html",data=data,product=product,message=message)


@app.route('/addoffer',methods=['GET', 'POST'])
@login_required
def addoffer():
    if(request.method=='POST'):
        discount = request.form['percentage']
        info = request.form['info']
        date=request.form['date']
        quantity = request.form['quantity']
        selectedProducts = request.form.getlist('selectedProducts')
        merchantID = session['merchantID']
        message = addoffersindb(mysql,merchantID,discount,info,date,quantity,selectedProducts)
        session['message_offer_add'] = message
    return redirect(url_for('showoffers'))


@app.route('/offers/edit/<OfferID>',methods=['GET', 'POST'])
@login_required
def editoffer(OfferID):
    merchantID = session['merchantID'] #get from session
    if(request.method=='GET'):
        offerID = OfferID
        data = getOffer(mysql,offerID)
        productChecked=[i['Name'] for i in list(data['Products'])]
        cur = mysql.connect.cursor()
        cur.execute("SELECT Name FROM Product WHERE MerchantID = '{}'".format(merchantID))
        productAll=[i['Name'] for i in list(cur.fetchall())]
        product = [x for x in productAll if x not in productChecked]
        return render_template("./manage_offers/editoffer.html",data=data,product=product,productChecked=productChecked,offerID = OfferID)
    else:
        discount = request.form['percentage']
        info = request.form['info']
        date=request.form['date']
        quantity = request.form['quantity']
        selectedProducts = request.form.getlist('selectedProducts')
        merchantID = session['merchantID']
        message = updateoffersindb(mysql,merchantID,discount,info,date,quantity,selectedProducts,OfferID)
        session['message_offer_add'] = message
        return redirect(url_for('showoffers'))


## TRANSACTION CONTROL MANAGEMENT ##
@app.route('/vtc', methods=['GET', 'POST'])
@login_required
def vtc():
    data=[]
    if('pan' in session):
        pan = session['pan']
    else:
        pan = None
    if('documentID' in session):
        documentID =session['documentID']
    else:
        documentID = None
    alertmsg = None
    categories = None
    msg = None
    if request.method=="POST":
        if not pan:
            try:
                pan = request.form['pan']
                session['pan'] = pan
            except:
                print('Pan not submitted')
        if(pan):
            try:
                if not documentID:
                    documentID = registerOnVTC(pan)
                session['documentID'] = documentID
                data = getMerchantControlRules(documentID)
                categories = getAvailableMerchantControls(pan)
            except:
                alertmsg = "Invalid Account Number"
                pan = None

        try:
            alertThreshold = request.form['alertThreshold']
            declineThreshold = request.form['declineThreshold']
            selectedCategory  = request.form.get('category')
            enabled = request.form.getlist('enabled')
            if(len(enabled)):
                enabled = "true"
            else:
                enabled = "false"
            decline = request.form.getlist('decline')

            if(len(decline)):
                decline = "true"
            else:
                decline = "false"
            controlRule = None
            if(selectedCategory == "global"):
                controlRuleString = '''
                {
                        "globalControls": [
                            {
                                "shouldDeclineAll": '''+decline+''',
                                "alertThreshold": '''+alertThreshold+''',
                                "isControlEnabled": '''+enabled+''',
                                "declineThreshold": '''+declineThreshold+'''
                            }
                        ]
                }

                '''
                controlRule = json.loads(controlRuleString)
            else:
                controlRuleString = '''
                {
                    "merchantControls": [
                    {
                        "shouldDeclineAll": '''+decline+''',
                        "isControlEnabled": '''+enabled+''',
                        "alertThreshold": '''+alertThreshold+''',
                        "declineThreshold": '''+declineThreshold+''',
                        "controlType": "'''+selectedCategory+'''"
                    }
                    ]

                }

                '''
                controlRule = json.loads(controlRuleString)
            
            documentID = session['documentID']
            
            if(controlRule):
                addMerchantControlRule(documentID,controlRule)
                msg = "yes"
        except Exception as e:
            print(e)
            alertmsg = "problem adding control"
    return render_template("./transactionControl/transactionControl.html",pan=pan,items=data,alertmsg=alertmsg,categories = categories,msg=msg)

if __name__ == '__main__':
    # threaded allows multiple users
    app.run(debug=True, threaded=True, port=5000)
