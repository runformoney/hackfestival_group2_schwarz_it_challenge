import csv
import os


def check_product_images(csv_file, image_dir):
    missing_images = []

    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row if present

        for row in csv_reader:
            if len(row) >= 2:  # Ensure row has at least 2 columns
                product_id = row[0]
                second_column_value = row[1]
                image_path = os.path.join(image_dir, f"{product_id}.jpg")

                if not os.path.isfile(image_path):
                    missing_images.append((product_id, second_column_value))

    return missing_images


# Usage
csv_file = "data/product_data.csv"
image_directory = "static/product_images/"

missing_product_images = check_product_images(csv_file, image_directory)

if missing_product_images:
    print("The following product IDs are missing images:")
    print("Product ID | Second Column Value")
    print("-----------|-----------------")
    for product_id, second_value in missing_product_images:
        print(f"{product_id:<11}| {second_value}")
else:
    print("All products have corresponding images.")
