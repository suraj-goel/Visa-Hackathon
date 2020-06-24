from functools import wraps
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import jinja2
import os
import uuid
from datetime import timedelta
from flask import Flask, render_template, request
from flask import *
from flask import session
from services.db.db_connection import set_connection
from search_merchants.searchMerchant import getCurrentLocation
from place_order.displayProduct import displayAllProducts, displayAllOffers
from search_merchants.searchProducts import getSearchResults
# from place_order.displayCart import displayALLCart
from login_registration.registerMerchant import checkIfExistingMerchant, registerNewMerchant, checkPayType
from login_registration.loginMerchant import checkEmailAndPassword
from accounts.validate_accounts import validation  # validate_accounts.py
from place_order.displayCart import addToCart
from manage_inventory.SearchInventory import *
from manage_inventory.addProduct import addNewProduct, getCategories
from manage_inventory.updateProduct import *
from orders_management.orderHistory import getOrders

app = Flask(__name__, static_folder='')
app.jinja_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader(['.'])])
app.config['GOOGLEMAPS_KEY'] = ""
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=5)
mysql = set_connection(app)
GoogleMaps(app)


# auth decorator
def login_required(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        if 'session_id' in session:
            id = session['session_id']
            if 'pay_type' in session:
                return function_to_protect(*args, **kwargs)
            elif checkPayType(mysql, id):
                session.permanent = True
                session['pay_type'] = True
                return redirect('/home')
            else:
                return redirect('/payment')
        else:
            flash("Please log in")
            return redirect(url_for('login'))
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
@login_required
def login():
    if request.method == 'POST':
        session.pop('session_id', None)

        username = request.form['username']
        password = request.form['password']

        users = checkEmailAndPassword(username,password)
        if len(users) >0:
            session.permanent = True
            session['session_id'] = users[0][0]
            return redirect(url_for('/home'))
        else:
            flash('Incorrect Email and Password combination')
            return redirect(url_for('login'))
        #user = [x for x in users if x.username == username][0]
        #if user and user.password == password:
        #    session['user_id'] = user.id
         #   return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template("./login_registration/login.html")

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        #session.pop('user_id', None)

        #username = request.form['username']
        #password = request.form['password']
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        if password != confirmPassword:
            flash('Passwords do not match')
            return redirect(url_for(request.url))

        if checkIfExistingMerchant(mysql,email):
            flash('Email already registered')
            return redirect(url_for(request.url))
        else:
            session.permanent = True
            id = registerNewMerchant(mysql, email, password, name)
            session['session_id'] = id

        return redirect(url_for('login'))

    return render_template("./login_registration/registration.html")

@app.route('/logout')
@login_required
def logout():
    session.pop('session_id', None)
    return redirect('/login')


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
    history = getOrders(mysql, merchantid)
    return render_template('./orders_management/order_management.html', history=history)


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
        session.clear()
        return redirect(url_for('showAll'))


@app.route('/accounts/', methods=['GET', 'POST'])
def displayaccountsdetails():
    cur = mysql.connection.cursor()
    cur.execute("select * from Merchant where MerchantID='2';")
    # "select * from Merchant where MerchantID ='"+str(session['Mercahntid'])+"';"
    result = cur.fetchone()
    cur.close()
    return render_template("./accounts/displayAccountDetails.html", result=result)


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


@app.route('/merchant/<merchant_id>/requirements')
def requirements(merchant_id):
    return render_template("./requirements/requirements.html")


if __name__ == '__main__':
    # threaded allows multiple users (for hosting)
    app.run(debug=True, threaded=True, port=5000)
