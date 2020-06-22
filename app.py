import jinja2
from flask import Flask, render_template, request
from flask import *
from services.db.db_connection import set_connection
from search_merchants.searchMerchant import getCurrentLocation
from place_order.displayProduct import displayAllProducts, displayAllOffers
from search_merchants.searchProducts import getSearchResults
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


if __name__ == '__main__':
    #threaded allows multiple users (for hosting)
    app.run(debug=True,threaded=True, port=5000)

