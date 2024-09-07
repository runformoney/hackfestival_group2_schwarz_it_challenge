import pandas as pd
import uuid
import random
from datetime import datetime, timedelta

# Load the products data from CSV
product_data = pd.read_csv('../data/product_data.csv')

# Convert 'expiresAt' to datetime
product_data['expiresAt'] = pd.to_datetime(product_data['expiresAt'])

# Calculate days until expiry
current_date = datetime.now()
product_data['days_until_expiry'] = (product_data['expiresAt'] - current_date).dt.days

# Identify products expiring within 30 days
expiring_products = product_data[product_data['days_until_expiry'] <= 30]
non_expiring_products = product_data[product_data['days_until_expiry'] > 30]

# Create dictionaries to map product names to IDs
expiring_product_ids = dict(zip(expiring_products['name'], expiring_products['id']))
non_expiring_product_ids = dict(zip(non_expiring_products['name'], non_expiring_products['id']))

# Parameters
n_customers = 1000  # 1,000 customers
n_transactions = 100000  # 100,000 transactions total
store_id = 101  # Store ID
discount_probability = 0.01  # 1% discount probability
expiring_product_percentage = 0.80  # 80% of transactions should be expiring products

# Generate transaction data
transactions = []
start_date = datetime.now() - timedelta(days=30)  # 1 month from now
end_date = datetime.now()


def random_timestamp():
    day_offset = random.randint(0, 29)  # Select a random day from the last 30 days
    time_of_day = random.randint(7 * 60, 22 * 60)  # Between 7:00 AM and 10:00 PM
    random_time = timedelta(minutes=time_of_day)
    random_date = start_date + timedelta(days=day_offset) + random_time
    return random_date


# Generate transactions
for _ in range(n_transactions):
    transaction_id = str(uuid.uuid4())
    customer_id = random.randint(1, n_customers)

    # Determine if this transaction should use an expiring product
    if random.random() < expiring_product_percentage:
        product_name = random.choice(list(expiring_product_ids.keys()))
        product_id = expiring_product_ids[product_name]
    else:
        product_name = random.choice(list(non_expiring_product_ids.keys()))
        product_id = non_expiring_product_ids[product_name]

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
transaction_df.to_csv('../data/transactions_80percent_expiring.csv', index=False)

print(f"Generated {len(transactions)} transactions with emphasis on expiring products.")

# Calculate and print statistics
expiring_count = transaction_df[transaction_df['product_name'].isin(expiring_product_ids.keys())].shape[0]
non_expiring_count = transaction_df[transaction_df['product_name'].isin(non_expiring_product_ids.keys())].shape[0]

print(f"Expiring products transactions: {expiring_count}")
print(f"Non-expiring products transactions: {non_expiring_count}")
print(f"Percentage of expiring products: {expiring_count / len(transactions) * 100:.2f}%")