import math
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# Sample data: ProductId and corresponding prices

product_data = pd.read_csv("data/product_data_with_carbon_footprint.csv")
product_data["popularity"] = 0.5

max_discount = 0.9


def price(productId):
    product = product_data.loc[product_data["id"] == productId]
    full_price = product["price"].values[0]
    expiry_date = product["expiresAt"].values[0]
    popularity = product["popularity"].values[0]
    available_stock = product["available"].values[0]

    print(f"popularity: {popularity}")
    # Convert dates to days since epoch for easy subtraction
    expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
    current_date = datetime.now()

    remaining_time = (expiry_date - current_date).total_seconds() / 86400
    return discounted_price(full_price, remaining_time, popularity, available_stock)


def discounted_price(full_price, remaining_time, popularity, available_stock):
    discount = discount_percent(remaining_time, popularity, available_stock)

    # Calculate final price
    final_price = full_price * (1 - discount)

    return round(float(final_price) * random.uniform(0.5, 1), 2)


def discount_percent(remaining_time, popularity, available_stock):
    decay_rate = (1.0 - popularity) * stock_factor(available_stock) * 4
    # print(f"decay_rate: {decay_rate}= ppop:{popularity} stock_factor: {stock_factor(available_stock)}")
    if remaining_time > 10:
        return 0
    # Calculate exponential discount
    if remaining_time > 0:
        discount = 1 - math.exp(-decay_rate * (1 / remaining_time))
    else:
        discount = 1
    # Ensure the discount is capped at 90%
    return min(discount, max_discount)


def stock_factor(stock_available):
    if stock_available >= 200 - (200 / 3):
        return 1.0
    elif stock_available >= 220 - 2 * (200 / 3):
        return 0.5
    else:
        return 0


######## testing and plotting:
def testPrice():
    full_price = 49.99
    for remaining_time in range(12, 0, -1):
        print(discounted_price(full_price, remaining_time, 0.5))


def plot():
    # x axis values
    x = [remaining_days for remaining_days in range(15, -1, -1)]
    print(x)
    # corresponding y axis values

    stock = 10
    for popularity in np.linspace(0.0, 1.0, 20, endpoint=True):
        print("###00" + str(popularity))
        y = [
            discount_percent(remaining_days, popularity, stock) for remaining_days in x
        ]
        plt.plot(x, y, label=f"popularity={popularity}")
        plt.title(f"stock={stock}")

    # naming the x axis
    plt.xlabel("remaining_days")
    # naming the y axis
    plt.ylabel("discounted in percent")
    plt.legend(loc="best")

    # Reverse the x-axis so it starts at 15 and ends at 0
    plt.xlim(15, 0)
    # Set tick marks on the x-axis
    plt.xticks(ticks=x)

    # function to show the plot
    plt.show()


if __name__ == "__main__":
    plot()
