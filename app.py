import jinja2
from flask import *
from flask import session
from services.db.db_connection import set_connection
from search_merchants.searchMerchant import getCurrentLocation
from place_order.displayProduct import displayAllProducts, displayAllOffers
from search_merchants.searchProducts import getSearchResults
from accounts.validate_accounts import validation  # validate_accounts.py
from place_order.displayCart import addToCart
from manage_inventory.SearchInventory import *
from manage_inventory.addProduct import addNewProduct, getCategories
from manage_inventory.updateProduct import *
from orders_management.orderHistory import getOrders
from requirements.requirements import *
from services.visa_api_services import register_merchant, paymentProcessing
from services.cybersourcePayment import simple_authorizationinternet
from manage_inventory.buyerUpdater import *
from requirements.showRequirements import getSupplierRequests, getBuyerRequests
from payment.confirmPayment import *
from manage_inventory.supplierupdater import *
app = Flask(__name__, static_folder='')
app.jinja_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader(['.'])])
app.secret_key = 'super secret key'
mysql = set_connection(app)


@app.route('/login')
def login():
    return render_template("./login_registration/login.html")


@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if request.method == 'POST':
        print(request.form)
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        category = request.form.get('category')
        if category == 'others':
            category = request.form['other_category']
        sell = request.form['sell']
        merchantID = 1
        message = addNewProduct(name, description, price, quantity, category, sell, merchantID, mysql)
        session['message_product_add'] = message
    return redirect(url_for('inventory'))


@app.route('/inventory/', methods=['POST', 'GET'])
def inventory():
    merchantid = 1
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


@app.route('/inventory/edit/<productID>', methods=['POST', 'GET'])
def editProduct(productID):
    merchantID = 1
    productID = productID
    c = getCategories(mysql)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        category = request.form.get('category')
        if category == 'others':
            category = request.form['other_category']
        sell = request.form['sell']
        merchantID = 1
        message = updateProduct(productID, merchantID, mysql, name, description, price, quantity, category, sell)
        session['message_product_add'] = message
        return redirect(url_for('inventory'))
    else:
        cur = mysql.connection.cursor()
        query = "SELECT * FROM Product WHERE ProductID = '{}'".format(productID)
        cur.execute(query)
        data = cur.fetchall()
        return render_template("./manage_inventory/editProduct.html", data=data[0], category=c, productID=productID)


@app.route('/orders', methods=['POST', 'GET'])
def orders():
    merchantid = 1
    delivered_filter = 'yes'
    selectedCartID = None
    if request.method == 'POST':

        if "filter" in request.form:
            delivered_filter = request.form['filter']
        if "confirm" in request.form:
            selectedCartID = request.form['confirm']
    if selectedCartID:
        cur = mysql.connection.cursor()
        cur.execute("Update Orders SET Status = 'yes' WHERE CartID = '{}'".format(selectedCartID))
        cur.execute("SELECT OrderID FROM Orders WHERE CartID = '{}'".format(selectedCartID))
        data = list(cur.fetchall())
        updateBuyerInventoryOrder(mysql, data[0]['OrderID'], merchantid)
    history = getOrders(mysql, merchantid, delivered_filter)
    return render_template('./orders_management/order_management.html', history=history, filter=delivered_filter)


@app.route('/', methods=['POST', 'GET'])
@app.route('/search', methods=['POST', 'GET'])
def showAll():
    currentMerchantID = 2
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


@app.route('/merchant/<merchant_id>', methods=['GET', 'POST'])
def showPlaceOrder(merchant_id):
    if request.method == 'GET':
        currentSelectedMerchantID = merchant_id
        # get the currentSelectedMerchantID from function
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
        session['mid'] = merchant_id
        print(session['discountPrice'])
        return redirect(url_for('showCart', merchant_id=merchant_id))


Check = False


def modify():
    global Check
    Check = True


@app.route("/merchant/<merchant_id>/cart", methods=['GET', 'POST'])
def showCart(merchant_id):
    totalQuantity = 0
    qty = []
    ProductID = []
    Name = []
    Description = []
    Price = []
    Offers = []
    discountPrice = []
    if request.method == 'GET':
        try:
            qty = session['qty']
            ProductID = session['ProductID']
            Name = session['Name']
            Description = session['Description']
            Price = session['Price']
            Offers = session['offers']
            discountPrice = session['discountPrice']
            l = len(qty)
            for i in qty:
                totalQuantity += int(i)
        except Exception as e:
            print("exception details " + str(e))

        return render_template("./place_order/cart.html", merchantID=merchant_id, qty=qty, ProductID=ProductID,
                               Name=Name, Description=Description, Price=Price, Offers=Offers,
                               discountPrice=discountPrice, len=len(qty), totalQuantity=totalQuantity)
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
        if (Check == False):
            addToCart(mysql, qty, ProductID, Name, Description, Price, merchant_id, status, finalPrice,
                      finalDiscountPrice, NegotitatedRequestAmount)
            modify()
        if(Type != 'Process Payment'):
            session.clear()
        return redirect(url_for('showAll'))


@app.route('/accounts/', methods=['GET', 'POST'])
def displayaccountsdetails():
    cur = mysql.connection.cursor()
    cur.execute("select * from PaymentType where MerchantID='2';")
    r = cur.fetchone()
    cur.execute("select * from Merchant where MerchantID='2';")
    # "select * from Merchant where MerchantID ='"+str(session['Mercahntid'])+"';"
    result = cur.fetchone()
    cur.close()
    if r == None:
        return render_template("./accounts/displayAccountDetails.html", result=result, b2bregistered=0,
                               cyberregistered=0)
    elif r['PayType'] == '1':
        return render_template("./accounts/displayAccountDetails.html", result=result, b2bregistered=0,
                               cyberregistered=1)
    elif r['PayType'] == '2':
        return render_template("./accounts/displayAccountDetails.html", result=result, b2bregistered=1,
                               cyberregistered=0)
    else:
        return render_template("./accounts/displayAccountDetails.html", result=result, b2bregistered=1,
                               cyberregistered=1)


@app.route('/editaccountinfo/', methods=['GET', 'POST'])
def editAccountDetails():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        mid = "2"  # session['mid']
        name = request.form['name']
        registeredName = request.form['registeredName']
        email = request.form['emailid']
        contactno = request.form['contactno']
        address = request.form['address']
        password = request.form['password']
        r = validation(mysql, mid, name, registeredName, email, contactno, address, password)

        if r[2] == 0:
            cur.execute(
                "update Merchant set Name = '" + name + "', RegisteredName = '" + registeredName + "', EmailID = '" + email + "', ContactNumber = '" + contactno + "', Address = '" + address + "', password = '" + password + "' where MerchantID='" + mid + "';")
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
            if (r[1][5]):
                flash("Password already exists, please enter a new one.")
            return render_template("./accounts/editAccountDetails.html", result=result)

    cur.execute("select * from Merchant where MerchantID='2'")
    # "select * from Merchant where MerchantID = '"+str(session['Merchantid'])+"';"
    result = cur.fetchone()
    cur.close()
    return render_template("./accounts/editAccountDetails.html", result=result)


@app.route('/registerB2B/<merchant_id>', methods=['GET', 'POST'])
def registerB2B(merchant_id):
    register_merchant(mysql, merchant_id)
    return redirect('/accounts/')


@app.route('/registerCyber/', methods=['GET', 'POST'])
def registerCyber():
    merchant_id = '2'  # retrieve from session
    cur = mysql.connection.cursor()
    cur.execute("select * from CybersourceMerchant where MerchantID='" + merchant_id + "';")
    result = cur.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        aggregatorID = request.form['aggregatorid']
        cardAcceptorID = request.form['cardacceptorid']
        if result == None:
            cur.execute(
                "insert into CybersourceMerchant(AggregatorID,CardAcceptorID,Name,MerchantID) values (%s,%s,%s,%s);",
                (aggregatorID, cardAcceptorID, name, merchant_id))
            cur.execute("select * from PaymentType where MerchantID='" + merchant_id + "';")
            r = cur.fetchone()
            if r == None:
                cur.execute("INSERT INTO PaymentType (MerchantID, PayType) VALUES (%s, %s);", (merchant_id, '1'))
            else:
                cur.execute("update PaymentType set PayType='3' where MerchantID='" + merchant_id + "';")
            mysql.connection.commit()
        else:
            cur.execute(
                "update CybersourceMerchant set Name = '" + name + "', AggregatorID = '" + aggregatorID + "', CardAcceptorID = '" + cardAcceptorID + "' where MerchantID='" + merchant_id + "';")
        mysql.connection.commit()
        return redirect('/accounts/')
    return render_template("./accounts/cyberSourceDetails.html", result=result)

@ app.route('/payments/',methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        amount = request.form['finalPrice']
    return render_template("./payment/payment.html", amount=amount)

@app.route('/cybersource/', methods=['GET', 'POST'])
def cybersource():
	merchant_id = "2"  # session['merchantID']

	qty=session['qty']
	ProductID=session['ProductID']
	Name = session['Name']
	Description =session['Description']
	Price = session['Price']
	Offers = session['offers']
	discountPrice = session['discountPrice']
	sellerId = session['mid']

	cur = mysql.connection.cursor()
	cur.execute("select AggregatorID,CardAcceptorID,Name from CybersourceMerchant where MerchantID='"+sellerId+"';")
	result = cur.fetchone()
	aggregatorID,cardAcceptorID,name = result['AggregatorID'],result['CardAcceptorID'],result['Name']

	if request.method == 'POST':
		print(request.form)
		amount = request.form.getlist('amount')[0]
		username = request.form.getlist('username')[0]
		cardNumber = request.form.getlist('cardNumber')[0]
		month = request.form.getlist('month')[0]
		year = request.form.getlist('year')[0]
		cvv = request.form.getlist('CVV')[0]
		status = simple_authorizationinternet(cardNumber,month,year,amount,aggregatorID,cardAcceptorID,username)
		# if payment in authorized then call ****
		# addToOrders(mysql,qty,ProductID,Name,Description,Price,sellerId,"no",discountPrice[0],discountPrice[0],'1-01-2012')
		# updateSupplierInventory(mysql,productList)

		# currentDate is today's date
		# merchantID is seller's id
		# status will be 'no'
		# check date format
		# pass the correct values recieved from session (refer this for more info @app.route("/merchant/<merchant_id>/cart",methods=['GET','POST']))

		return redirect(url_for('showAll'))
	return render_template("./payment/payment.html",amount=amount)


@app.route('/negotiation',methods=['GET','POST'])
def negotiation():
    if(request.method=='GET'):
        merchant_id = 1 #get from seearch
        return render_template("./negotiation/negotiation.html")

@app.route('/requirementssupplier', methods=['GET', 'POST'])
def showsupplierrequirements():
	merchantid = 3
	items = getSupplierRequests(mysql, merchantid)
	choice = 'P'
	if request.method == 'POST':
		choice = request.form['filtersupplier']
		items = getSupplierRequests(mysql, merchantid, choice)
	return render_template('./requirements/requirements.html', sup_items=items, choice=choice, profile=2)


@app.route('/requirementsbuyer', methods=['GET', 'POST'])
def showbuyerrequirements():
	merchantid = 1
	items = getSupplierRequests(mysql, merchantid)
	choice = 'R'
	if request.method == 'POST':
		choice = request.form['filterbuyer']
		items = getBuyerRequests(mysql, merchantid, choice)
		print(items)
	return render_template('./requirements/requirements.html', buy_items=items, buyer_choice=choice, profile=3)


@app.route('/requirements', methods=['GET', 'POST'])
def requirements():
	if (request.method == 'GET'):
		merchant_id = 3  # get from session
		registeredName = showBusinessName(mysql, merchant_id)
		return render_template("./requirements/requirements.html", registeredName=registeredName, profile=1)
	else:
		merchant_id = 3  # get from session
		title = request.form.get('title')
		description = request.form.get('description')
		quantity = request.form.get('Quantity')
		price = request.form.get('price')
		status = "Post"
		saveRequirements(mysql, merchantID=merchant_id, title=title, description=description, quantity=quantity,
                         price=price, status=status)
		return redirect(request.url)


if __name__ == '__main__':
	# threaded allows multiple users (for hosting)
	app.run(debug=True, threaded=True, port=5000)
