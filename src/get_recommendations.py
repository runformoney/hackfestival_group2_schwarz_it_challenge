import pickle
from scipy.sparse import csr_matrix
import pandas as pd
from src.config import PRODUCT_BUNDLES
import random
from src.price_calculator import price
import datetime


def convert_date(__date):
    return datetime.datetime.strptime(__date, '%Y-%m-%d').strftime('%d.%m.')


PRODUCT_DATA = pd.read_csv("data/product_data_with_carbon_footprint.csv")
PRODUCT_DATA.expiresAt = PRODUCT_DATA.expiresAt.apply(convert_date)
PRODUCT_DATA_DICT = dict(zip(PRODUCT_DATA['id'],
                             PRODUCT_DATA[['id', 'name',
                                           'price', 'carbon_footprint', 'expiresAt']].values.tolist()))


# Load the saved ALS model from "../model" folder
def load_model():
    with open('model/als_model.pkl', 'rb') as f:
        return pickle.load(f)


# Load the interaction matrix, customer_map, and product_map from "../model" folder
def load_data():
    # Load the interaction matrix and convert it to CSR format for fast row slicing
    with open('model/interaction_matrix.pkl', 'rb') as f:
        interaction_matrix = pickle.load(f).tocsr()  # Convert to CSR format

    with open('model/customer_map.pkl', 'rb') as f:
        customer_map = pickle.load(f)

    with open('model/product_map.pkl', 'rb') as f:
        product_map = pickle.load(f)

    return interaction_matrix, customer_map, product_map


# Function to recommend products for a given customer ID
def recommend_products(customer_index, num_recommendations=20):
    if customer_index is None:
        return "Customer not found"

    user_interaction = INTERACTION_MATRIX[0]

    # Get recommendations using the ALS model
    recommendations = MODEL.recommend(customer_index, user_interaction, N=num_recommendations)

    # Filter out invalid recommendations and map back the recommended product indices to product IDs
    recommended_product_ids = []
    for product_idx in recommendations[0]:
        # Ensure the product index is valid and exists in product_map
        if product_idx in PRODUCT_MAP:
            recommended_product_ids.append(PRODUCT_MAP[product_idx])
        else:
            print(f"Invalid product index: {product_idx}")

    return recommended_product_ids if recommended_product_ids else "No valid recommendations"

def get_product_data(product_id):
    product_data = PRODUCT_DATA_DICT.get(product_id)
    product_data.insert(3, price(product_id))

    return product_data

def get_all_recos(customer_index):
    personalized_recos = recommend_products(customer_index)
    product_bundle = random.sample(PRODUCT_BUNDLES, 10)[0]

    personalized_recos_with_product_data = [get_product_data(__id) for __id in personalized_recos]
    product_bundle_with_product_data = [get_product_data(product_info[0]) for product_info in product_bundle]

    return {"personalized_recos": personalized_recos_with_product_data,
            'product_bundle': product_bundle_with_product_data}




MODEL = load_model()
INTERACTION_MATRIX, CUSTOMER_MAP, PRODUCT_MAP = load_data()

if __name__ == '__main__':
    print(get_all_recos(1))
