import pandas as pd
import uuid
import random
from datetime import datetime, timedelta

# Load the products data from CSV (assuming it's already loaded in a variable)
product_data = pd.read_csv('data/product_data.csv')

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


# Grouping of products (based on product names)
product_groups = {
    'Vegetables': ['Organic Cherry Tomatoes', 'Sweet Potatoes', 'Broccoli Florets', 'Red Bell Peppers'],
    'Greens': ['Baby Spinach']
}

# Generating customer transaction counts (1 to 10 transactions per customer)
customer_transaction_counts = [random.randint(1, 10) for _ in range(n_customers)]
customer_ids = [str(uuid.uuid4()) for _ in range(n_customers)]

# Adjust the total transaction count to match exactly 100,000 transactions
total_transactions = sum(customer_transaction_counts)
adjust_factor = n_transactions / total_transactions
customer_transaction_counts = [int(count * adjust_factor) for count in customer_transaction_counts]

# Ensure exactly 100k transactions by adjusting a few values
diff = n_transactions - sum(customer_transaction_counts)
for i in range(diff):
    customer_transaction_counts[i % n_customers] += 1

# Creating transaction data
for customer_id, count in zip(customer_ids, customer_transaction_counts):
    for _ in range(count):
        transaction_id = str(uuid.uuid4())

        # Randomly select a product group and product from that group
        group = random.choice(list(product_groups.keys()))
        product_name = random.choice(product_groups[group])
        product = product_data[product_data['name'] == product_name].iloc[0]

        # Prepare transaction details
        product_id = product['id']
        price = product['price']

        # Apply discount to 1% of products
        is_discount_applied = 1 if random.random() < discount_probability else 0

        # Generate a random timestamp
        timestamp = random_timestamp()

        # Create transaction entry
        transactions.append({
            'transaction_id': transaction_id,
            'customer_id': customer_id,
            'product_id': product_id,
            'price': price,
            'filiale': store_id,
            'timestamp': timestamp,
            'is_discount_applied': is_discount_applied,
            'popularity': (random.random()),
            'carbon_footprint': (random.uniform(50, 5000))
        })

# Create DataFrame from the transactions list
transactions_df = pd.DataFrame(transactions)

# Save the transaction data to a CSV file
transactions_df.to_csv('data/customer_transactions_100k.csv', index=False)

print("Transaction data generated and saved to 'customer_transactions_100k.csv'.")
