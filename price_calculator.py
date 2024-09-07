import math
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data: ProductId and corresponding prices

product_data = pd.read_csv('data/product_data.csv')
product_data['popularity']=0.5

max_discount = 0.9

def price(productId):
    product = product_data.loc[product_data['id']==productId]
    full_price = product['price'].values[0]
    expiry_date = product['expiresAt'].values[0]
    popularity = product['popularity'].values[0]
    print(f"popularity: $popularity")
    # Convert dates to days since epoch for easy subtraction
    expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
    current_date = datetime.now()

    remaining_time = (expiry_date - current_date).days
    return discounted_price(full_price, remaining_time, popularity)


def discounted_price(full_price, remaining_time, popularity):
    discount = discount_percent(remaining_time, (1.0 - popularity))

    # Calculate final price
    final_price = full_price * (1 - discount)

    return final_price

def discount_percent(remaining_time, decay_rate):
    if remaining_time > 10:
        return 0
    # Calculate exponential discount
    if remaining_time > 0:
        discount = (1 - math.exp(-decay_rate * (1 / remaining_time)))
    else:
        discount = 1
    # Ensure the discount is capped at 90%
    return min(discount, max_discount)


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

    for decay_rate in np.linspace(0, 1, 10, endpoint=True):
        y = [discount_percent(remaining_days, decay_rate) for remaining_days in x]
        plt.plot(x, y, label=decay_rate)

    # naming the x axis
    plt.xlabel('remaining_days')
    # naming the y axis
    plt.ylabel('discounted in percent')
    plt.legend(loc='best')

    # Reverse the x-axis so it starts at 15 and ends at 0
    plt.xlim(15, 0)
    # Set tick marks on the x-axis
    plt.xticks(ticks=x)

    # function to show the plot
    plt.show()


# testPrice()
# plot()
price(9126483)