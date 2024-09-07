from flask import Flask, render_template
from src import get_recommendations
import random
import price_calculator

app = Flask(__name__)

@app.route('/')
def mainpage():
    return render_template("mainpage.html")

@app.route('/discount')
def discount():
    customer_index= random.randint(0, 999)
    recos = get_recommendations.get_all_recos(customer_index)

    return render_template("discount.html",
                           discount=recos['product_bundle'])

@app.route('/bundle')
def bundle():
    return render_template("bundle.html")


@app.route('/product/<productId>/price', methods=['GET'])
def get_product_price(productId):
    return str(price_calculator.price(productId)),200


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)