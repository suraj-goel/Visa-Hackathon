import jinja2
from flask import Flask, render_template
from services.db.db_connection import set_connection
from search_merchants.searchMerchant import getAllMerchants
from place_order.displayProduct import displayAllProducts
app=Flask(__name__)

app = Flask(__name__,static_folder = 'common')
app.jinja_loader = jinja2.ChoiceLoader([app.jinja_loader,jinja2.FileSystemLoader(['.'])])


mysql = set_connection(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("select * from hello;")
    a=cur.fetchall()
    cur.close()
    return render_template("./manage_inventory/inventory.html", name=a[1]['name'])

@app.route('/login')
def login():
    return render_template("./login_registration/login.html")

@app.route('/home')
def showAll():
    currentMerchantID = 1
    # get the currentMerchantID from session. 
    merchants = getAllMerchants(mysql,currentMerchantID)
    print(merchants)
    return render_template("./merchant_home_page/home.html",merchants = merchants)


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
