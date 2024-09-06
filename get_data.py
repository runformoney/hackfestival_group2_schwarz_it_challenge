import requests
import json
import os

os.makedirs("data", exist_ok=True)

# Example API URL
url = "https://hackathon-products-api.apps.01.cf.eu01.stackit.cloud/api/articles"

# Make the GET request
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Convert response to JSON
    data = response.json()

    # Save data to a JSON file
    import pandas as pd

    pd.DataFrame(data).to_csv("data/product_data.csv", index=False)

    print("Data saved to 'data.json'.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
