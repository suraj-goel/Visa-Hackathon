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
    if request.method == "POST":
        product = request.form['product']
        data=getSearchResults(mysql,product, currentMerchantID)
        return render_template('./search_merchants/search.html', data=data,product=product)
    # get the currentMerchantID from session.
    print(getAllMerchants(mysql,currentMerchantID))
    return render_template("./search_merchants/search.html")


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
