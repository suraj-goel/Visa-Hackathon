import jinja2
import os
from flask import Flask, render_template, request
from flask import *
from services.db.db_connection import set_connection
from search_merchants.searchMerchant import getCurrentLocation
from place_order.displayProduct import displayAllProducts, displayAllOffers
from search_merchants.searchProducts import getSearchResults
from place_order.displayCart import displayALLCart
from login_registration.registerMerchant import checkIfExistingMerchant,registerNewMerchant
from login_registration.loginMerchant import checkEmailAndPassword
app = Flask(__name__,static_folder = '')
app.jinja_loader = jinja2.ChoiceLoader([app.jinja_loader,jinja2.FileSystemLoader(['.'])])

app.secret_key = os.urandom(24)
mysql = set_connection(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('session_id', None)

        username = request.form['username']
        password = request.form['password']

        users = checkEmailAndPassword(username,password)
        if len(users) >0:
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
            registerNewMerchant(mysql,email,password,name)

        return redirect(url_for('login'))

    return render_template("./login_registration/registration.html")

@app.route('/logout')
def logout():
    session.pop('session_id', None)
    return redirect('/login')


@app.route('/' ,methods=['POST','GET'])
@app.route('/search', methods=['POST','GET'])
def showAll():
    currentMerchantID = 2
    currentLocation = getCurrentLocation(mysql,currentMerchantID)
    if request.method == "POST":
        search_option = request.form['search']
        filter=request.form.get('offerbox')
        radius=request.form['radius']
        product = request.form['name']
        data=getSearchResults(mysql, currentMerchantID,product,search_option,filter, radius)
        return render_template('./search_merchants/search.html', data=data ,currentLocation = currentLocation, search_option=search_option)
    data = getSearchResults(mysql,currentMerchantID)
    return render_template("./search_merchants/search.html",currentLocation = currentLocation,data=data)


@app.route('/merchant/<merchant_id>',methods=['GET','POST'])
def showPlaceOrder(merchant_id):
    if request.method == 'GET':
        currentSelectedMerchantID = merchant_id
        #get the currentSelectedMerchantID from function
        products = displayAllProducts(mysql, currentSelectedMerchantID)
        offers = displayAllOffers(mysql, currentSelectedMerchantID)
        return render_template("./place_order/place_order.html", products = products, offers = offers ,len=len(products),merchantID=merchant_id)
    else:
        print(request.form)
        return redirect(request.url+"/cart")


@app.route("/merchant/<merchant_id>/cart",methods=['GET','POST'])
def showCart(merchant_id):
    currentMerchantID = merchant_id
    currentCartID = merchant_id
    carts = displayALLCart(mysql,cartID=currentCartID,merchantID=currentMerchantID)
    return render_template("./place_order/cart.html",merchantID=merchant_id,cartITEM=carts)


if __name__ == '__main__':
    #threaded allows multiple users (for hosting)
    app.run(debug=True,threaded=True, port=5000)

