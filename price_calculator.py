import math
from datetime import datetime
import pandas as pd

import matplotlib.pyplot as plt

# Sample data: ProductId and corresponding prices

product_data = pd.read_csv('data/product_data.csv')

max_discount=0.9
decay_rate = 1

def price(productId):
    full_price = product_data['price']
    expiry_date = product_data['expiresAt']

    # Convert dates to days since epoch for easy subtraction
    expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
    current_date = datetime.now()

    remaining_time = (expiry_date - current_date).days
    return discounted_price(full_price, remaining_time)

def discounted_price(full_price, remaining_time):
    if remaining_time > 10:
        return full_price

    # Calculate exponential discount
    if remaining_time>0:
        discount = max_discount * (1 - math.exp(-decay_rate * (1/remaining_time)))
    else:
        discount=1

    # Ensure the discount is capped at 90%
    if discount > max_discount:
        discount = max_discount

    # Calculate final price
    final_price = full_price * (1 - discount)

    return final_price



######## testing and plotting:

full_price=49.99
def testPrice():
    print("full_price: $full_price")

    for remaining_time in range(12,0, -1):
        print(discounted_price(full_price, remaining_time))



def plot():
    # x axis values
    x = [remaining_days for remaining_days in range(15,-1,-1)]
    print(x)
    # corresponding y axis values
    y = [discounted_price(full_price, remaining_days) for remaining_days in x]
    print(y)

    # plotting the points
    plt.plot(x, y)

    # naming the x axis
    plt.xlabel('remaining_days')
    # naming the y axis
    plt.ylabel('discounted price')

    # Reverse the x-axis so it starts at 15 and ends at 0
    plt.xlim(15, 0)

    # Set tick marks on the x-axis
    plt.xticks(ticks=x)

    # function to show the plot
    plt.show()

# testPrice()
if __name__ == '__main__':
    plot()
