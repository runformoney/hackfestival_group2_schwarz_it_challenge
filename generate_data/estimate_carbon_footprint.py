import pandas as pd

# Load the product data CSV
product_data = pd.read_csv('../data/product_data.csv')

# Fix the issue where '1k' appears instead of '1kg'
product_data['weight'] = product_data['weight'].replace('1k', '1kg')

# Function to estimate carbon footprint based on product characteristics
def estimate_carbon_footprint(row):
    # Base footprint (per kg)
    base_footprint = 0.5  # in kgCO2e per kg for fresh produce
    organic_multiplier = 0.8 if "Organic" in row['name'] else 1.0  # organic typically has lower footprint
    packaging_multiplier = 1.2 if row['packagingUnit'] in ['punnet', 'bag'] else 1.0  # packaging increases footprint

    try:
        # Convert weight to kg for consistent calculation
        if 'g' in row['weight']:
            weight_in_kg = float(row['weight'].replace('g', '')) / 1000
        else:
            weight_in_kg = float(row['weight'].replace('kg', ''))
    except ValueError:
        # Handle unexpected weight format by setting to 0
        weight_in_kg = 0

    # Estimated footprint calculation
    carbon_footprint = base_footprint * weight_in_kg * organic_multiplier * packaging_multiplier
    return carbon_footprint

# Apply the function to generate the carbon footprint for each product
product_data['carbon_footprint'] = product_data.apply(estimate_carbon_footprint, axis=1)

# Save the updated product data to a new CSV
product_data.to_csv('../data/product_data_with_carbon_footprint.csv', index=False)

# Display the first few rows to verify
print(product_data.head())
