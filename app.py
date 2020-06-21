import jinja2
from flask import Flask, render_template, request
from services.db.db_connection import set_connection
from search_merchants.searchMerchant import getAllMerchants
from search_merchants.searchMerchant import getCurrentLocation
from place_order.displayProduct import displayAllProducts, displayAllOffers
from search_merchants.searchProducts import getSearchResults


app = Flask(__name__,static_folder = '')
app.jinja_loader = jinja2.ChoiceLoader([app.jinja_loader,jinja2.FileSystemLoader(['.'])])


mysql = set_connection(app)

@app.route('/login')
def login():
    return render_template("./login_registration/login.html")

@app.route('/' ,methods=['POST','GET'])
@app.route('/search', methods=['POST','GET'])
def showAll():
    # get the currentMerchantID from session.
    currentMerchantID = 2
    data = getAllMerchants(mysql, currentMerchantID)
    currentLocation = getCurrentLocation(mysql,currentMerchantID)
    if request.method == "POST":
        search_option = request.form['search']
        filter=request.form.get('offerbox')
        radius=request.form['radius']
        product = request.form['name']
        data=getSearchResults(mysql,product, currentMerchantID,search_option,filter, radius)
        return render_template('./search_merchants/search.html', data=data, product=product ,currentLocation = currentLocation, search_option=search_option)
    return render_template("./search_merchants/search.html",currentLocation = currentLocation,data=data)


@app.route('/merchant/<merchant_id>')
def showPlaceOrder(merchant_id):
    currentSelectedMerchantID = merchant_id
    # get the currentSelectedMerchantID from function
    products = displayAllProducts(mysql, currentSelectedMerchantID)
    offers = displayAllOffers(mysql, currentSelectedMerchantID)
    return render_template("./place_order/place_order.html", products = products, offers = offers)


if __name__ == '__main__':
    #threaded allows multiple users (for hosting)
    app.run(debug=True,threaded=True, port=5000)

