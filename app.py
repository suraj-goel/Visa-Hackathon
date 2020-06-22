import jinja2

from flask import Flask, render_template, request, redirect,flash,session
from flask import *
from services.db.db_connection import set_connection
from search_merchants.searchMerchant import getCurrentLocation
from place_order.displayProduct import displayAllProducts, displayAllOffers
from search_merchants.searchProducts import getSearchResults

from accounts.validate_accounts import validation #validate_accounts.py
app=Flask(__name__)
app.secret_key = 'super secret key'
from place_order.displayCart import displayALLCart
app = Flask(__name__,static_folder = '')
app.jinja_loader = jinja2.ChoiceLoader([app.jinja_loader,jinja2.FileSystemLoader(['.'])])


mysql = set_connection(app)


@app.route('/login')
def login():
    return render_template("./login_registration/login.html")

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
        return redirect(url_for('showCart',merchant_id=merchant_id))


@app.route("/merchant/<merchant_id>/cart",methods=['GET','POST'])
def showCart(merchant_id):
    print(request.form)
    currentMerchantID = merchant_id
    currentCartID = merchant_id
    carts = displayALLCart(mysql,cartID=currentCartID,merchantID=currentMerchantID)
    return render_template("./place_order/cart.html",merchantID=merchant_id,cartITEM=carts)


@app.route('/accounts/', methods=['GET','POST'])
def displayaccountsdetails():
	cur = mysql.connection.cursor()
	cur.execute("select * from Merchant where MerchantID='2';")
	#"select * from Merchant where MerchantID ='"+str(session['Mercahntid'])+"';"
	result = cur.fetchone()
	cur.close()
	return render_template("./accounts/displayAccountDetails.html",result=result)

@app.route('/editaccountinfo/', methods=['GET','POST'])
def editAccountDetails():
	cur = mysql.connection.cursor()
	if request.method == 'POST':
		mid = "2" #session['mid']
		name = request.form['name']
		registeredName = request.form['registeredName']
		email = request.form['emailid']
		contactno = request.form['contactno']
		address = request.form['address']
		password = request.form['password']
		r = validation(mysql,mid,name,registeredName,email,contactno,address,password)

		if r[2]==0:
			cur.execute("update Merchant set Name = '"+name+"', RegisteredName = '"+registeredName+"', EmailID = '"+email+"', ContactNumber = '"+contactno+"', Address = '"+address+"', password = '"+password+"' where MerchantID='"+mid+"';")
			mysql.connection.commit()
			return redirect('/accounts/')
		else:
			result = r[0]
			"""if(r[1][0]):
				flash("Name already exists, please enter a new one.")
			if(r[1][1]):
				flash("Registered Name already exists, please enter a new one.")
			if(r[1][2]):
				flash("Email already exists, please enter a new one.")
			if(r[1][3]):
				flash("Contact Number already exists, please enter a new one.")
			if(r[1][4]):
				flash("Address already exists, please enter a new one.")
			if(r[1][5]):
				flash("Password already exists, please enter a new one.")"""
			return render_template("./accounts/editAccountDetails.html",result=result)

	cur.execute("select * from Merchant where MerchantID='2'")
	#"select * from Merchant where MerchantID = '"+str(session['Merchantid'])+"';"
	result = cur.fetchone()
	cur.close()
	return render_template("./accounts/editAccountDetails.html",result=result)


if __name__ == '__main__':
    #threaded allows multiple users (for hosting)
	app.run(debug=True,threaded=True, port=5000)

