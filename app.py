import jinja2
from flask import *
from flask import session
from services.db.db_connection import set_connection
from search_merchants.searchMerchant import getCurrentLocation
from place_order.displayProduct import displayAllProducts, displayAllOffers
from search_merchants.searchProducts import getSearchResults
from accounts.validate_accounts import validation #validate_accounts.py
from place_order.displayCart import addToCart
from services.visa_api_services import register_merchant,paymentProcessing

app = Flask(__name__,static_folder = '')
app.jinja_loader = jinja2.ChoiceLoader([app.jinja_loader,jinja2.FileSystemLoader(['.'])])
app.secret_key = 'super secret key'
mysql = set_connection(app)
Check=False
def modify():
	global Check
	Check = True
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
		session['qty']=request.form.getlist("qty[]")
		session['ProductID']=request.form.getlist("ProductID[]")
		session['Name'] = request.form.getlist("Name[]")
		session['Description'] = request.form.getlist("Description[]")
		session['Price'] = request.form.getlist("Price[]")
		session['offers'] = request.form.getlist("offers[]")
		session['discountPrice'] = request.form.getlist("discountPrice[]")
		print(session['discountPrice'])
		return redirect(url_for('showCart',merchant_id=merchant_id))


@app.route("/merchant/<merchant_id>/cart",methods=['GET','POST'])
def showCart(merchant_id):
	qty=[]
	ProductID=[]
	Name = []
	Description =[]
	Price =[]
	Offers = []
	discountPrice = []
	totalQuantity = 0
	if request.method=='GET':
		qty=session['qty']
		ProductID=session['ProductID']
		Name = session['Name']
		Description =session['Description']
		Price = session['Price']
		Offers = session['offers']
		discountPrice = session['discountPrice']
		l=len(qty)
		for i in qty:
			totalQuantity+=int(i)
		print(totalQuantity)
		return render_template("./place_order/cart.html",merchantID=merchant_id,qty=qty,ProductID=ProductID,Name=Name,Description=Description,Price=Price,Offers=Offers,discountPrice=discountPrice,len=len(qty),totalQuantity=totalQuantity)
	else:
		ProductID = request.form.getlist("ProductId[]")
		qty = request.form.getlist("qty[]")
		Name = request.form.getlist("Name[]")
		Description = request.form.getlist("Description[]")
		Price = request.form.getlist("discountPrice[]")
		Type = request.form.get("type")
		finalPrice = request.form.get('finalPrice')
		finalDiscountPrice = request.form.get('finalDiscountPrice')
		status ='N'
		if(Type == 'Process Payment'):
			status = 'P'
		if(Check==False):
			addToCart(mysql,qty,ProductID,Name,Description,Price,merchant_id,status,finalPrice,finalDiscountPrice)
			modify()

		return redirect(url_for('showCart',merchant_id=merchant_id))


@app.route('/accounts/', methods=['GET','POST'])
def displayaccountsdetails():
	cur = mysql.connection.cursor()
	cur.execute("select * from PaymentType where MerchantID='2';")
	r = cur.fetchone()
	cur.execute("select * from Merchant where MerchantID='2';")
	# "select * from Merchant where MerchantID ='"+str(session['Mercahntid'])+"';"
	result = cur.fetchone()
	cur.close()
	if r==None:
		return render_template("./accounts/displayAccountDetails.html",result=result,b2bregistered=0,cyberregistered=0)
	elif r['PayType']=='1':
		return render_template("./accounts/displayAccountDetails.html", result=result,b2bregistered=0,cyberregistered=1)
	elif r['PayType']=='2':
		return render_template("./accounts/displayAccountDetails.html", result=result,b2bregistered=1,cyberregistered=0)
	else:
		return render_template("./accounts/displayAccountDetails.html", result=result, b2bregistered=1,cyberregistered=1)


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
			if(r[1][0]):
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
				flash("Password already exists, please enter a new one.")
			return render_template("./accounts/editAccountDetails.html",result=result)

	cur.execute("select * from Merchant where MerchantID='2'")
	#"select * from Merchant where MerchantID = '"+str(session['Merchantid'])+"';"
	result = cur.fetchone()
	cur.close()
	return render_template("./accounts/editAccountDetails.html",result=result)

@app.route('/registerB2B/<merchant_id>', methods=['GET','POST'])
def registerB2B(merchant_id):
	register_merchant(mysql,merchant_id)
	return redirect('/accounts/')

@app.route('/registerCyber/', methods=['GET','POST'])
def registerCyber():
	merchant_id = '2'  # retrieve from session
	cur = mysql.connection.cursor()
	cur.execute("select * from CybersourceMerchant where MerchantID='" + merchant_id + "';")
	result = cur.fetchone()
	if request.method == 'POST':
		name = request.form['name']
		aggregatorID = request.form['aggregatorid']
		cardAcceptorID = request.form['cardacceptorid']
		if result==None:
			cur.execute("insert into CybersourceMerchant(AggregatorID,CardAcceptorID,Name,MerchantID) values (%s,%s,%s,%s);", (aggregatorID,cardAcceptorID,name,merchant_id))
			cur.execute("select * from PaymentType where MerchantID='" + merchant_id + "';")
			r = cur.fetchone()
			if r == None:
				cur.execute("INSERT INTO PaymentType (MerchantID, PayType) VALUES (%s, %s);", (merchant_id, '1'))
			else:
				cur.execute("update PaymentType set PayType='3' where MerchantID='"+merchant_id+"';")
			mysql.connection.commit()
		else:
			cur.execute("update CybersourceMerchant set Name = '" + name + "', AggregatorID = '" + aggregatorID + "', CardAcceptorID = '" + cardAcceptorID + "' where MerchantID='" + merchant_id + "';")
		mysql.connection.commit()
		return redirect('/accounts/')
	return render_template("./accounts/cyberSourceDetails.html",result=result)


if __name__ == '__main__':
	#threaded allows multiple users (for hosting)
	app.run(debug=True,threaded=True, port=5000)

