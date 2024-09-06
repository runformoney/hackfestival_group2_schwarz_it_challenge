from flask import Flask, render_template

import price_calculator

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/product/<productId>/price', methods=['GET'])
def get_product_price(productId):
    return str(price_calculator.price(productId)),200


if __name__ == "__main__":
    app.run()