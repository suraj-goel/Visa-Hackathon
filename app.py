import jinja2
from flask import Flask, render_template, request
from services.db.db_connection import set_connection
from search_merchants.searchMerchant import getAllMerchants
from place_order.displayProduct import displayAllProducts
from search_merchants.searchProducts import getSearchResults
app=Flask(__name__)

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
    merchants = getAllMerchants(mysql, currentMerchantID)
    if request.method == "POST":
        search_option = request.form['search']
        filter=request.form.get('offerbox')
        radius=request.form['radius']
        product = request.form['name']
        data=getSearchResults(mysql,product, currentMerchantID,search_option,filter, radius)
        return render_template('./search_merchants/search.html', data=data, product=product, merchants=merchants , search_option=search_option)
    # get the currentMerchantID from session.

    return render_template("./search_merchants/search.html",merchants=merchants)


@app.route('/home/place_order')
def showPlaceOrder():
    currentSelectedMerchantID = 1
    # get the currentSelectedMerchantID from session. 
    products = displayAllProducts(mysql, currentSelectedMerchantID)
    for r in products:
        print(r)
    return render_template("./place_order/place_order.html", products = products)


if __name__ == '__main__':
    #threaded allows multiple users (for hosting)
    app.run(debug=True,threaded=True, port=5000)

