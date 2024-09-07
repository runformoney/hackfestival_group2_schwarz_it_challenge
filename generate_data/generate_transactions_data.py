import pandas as pd
import uuid
import random
from datetime import datetime, timedelta

# Load the products data from CSV
product_data = pd.read_csv('data/product_data.csv')

# Create a dictionary to map product names to IDs
product_ids = dict(zip(product_data['name'], product_data['id']))

# Parameters
n_customers = 1000  # 1,000 customers
n_transactions = 100000  # 100,000 transactions total
store_id = 101  # Store ID
discount_probability = 0.01  # 1% discount probability

# Generate transaction data
transactions = []
start_date = datetime.now() - timedelta(days=30)  # 1 month from now
end_date = datetime.now()


# Helper function to generate a random timestamp between Monday and Saturday, 7:00 AM to 10:00 PM
def random_timestamp():
    day_offset = random.randint(0, 29)  # Select a random day from the last 30 days
    time_of_day = random.randint(7 * 60, 22 * 60)  # Between 7:00 AM and 10:00 PM
    random_time = timedelta(minutes=time_of_day)
    random_date = start_date + timedelta(days=day_offset) + random_time
    return random_date


# Ensure all product names are represented
product_names = list(product_ids.keys())

# Generate transactions
for _ in range(n_transactions):
    transaction_id = str(uuid.uuid4())
    customer_id = random.randint(1, n_customers)
    product_name = random.choice(product_names)

    if product_name in product_ids:
        product_id = product_ids[product_name]
    else:
        continue  # Skip if the product name is not in the product_ids dictionary

    quantity = random.randint(1, 5)
    unit_price = random.uniform(1.0, 50.0)
    discount = 0.0

    if random.random() < discount_probability:
        discount = random.uniform(0.05, 0.30)  # Discount between 5% and 30%

    total_price = quantity * unit_price * (1 - discount)
    transaction_date = random_timestamp()

    transactions.append({
        'transaction_id': transaction_id,
        'store_id': store_id,
        'customer_id': customer_id,
        'product_id': product_id,
        'product_name': product_name,
        'quantity': quantity,
        'unit_price': unit_price,
        'discount': discount,
        'total_price': total_price,
        'transaction_date': transaction_date
    })

# Convert to DataFrame
transaction_df = pd.DataFrame(transactions)

# Save to CSV
transaction_df.to_csv('data/transactions.csv', index=False)

print(f"Generated {len(transactions)} transactions.")
