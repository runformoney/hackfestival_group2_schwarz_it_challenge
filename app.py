from flask import Flask, render_template
from src import get_recommendations
import random
import datetime
app = Flask(__name__)


@app.route('/')
def mainpage():
    return render_template("mainpage.html")

@app.route('/discount')
def discount():
    customer_index= random.randint(0, 999)
    recos = get_recommendations.get_all_recos(customer_index)

    print(recos)
    return render_template("discount.html",
                           discount=recos['product_bundle'],
                           products=recos['personalized_recos'],
                           now=datetime.now().strftime("%d.%m."))

@app.route('/bund')
def bundle():
    return render_template("bundle.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)