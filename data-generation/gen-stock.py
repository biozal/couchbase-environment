import json
import uuid
from random import randint
import zipfile
import os


# Define a function to decompress a file
def decompress_file(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('../couchbase-server/')
        return os.path.splitext(file_path)[0]  # return the file path without .zip


# Load the JSON data
warehouse_file_path = decompress_file('../couchbase-server/sample-warehouses.json.zip')
with open(warehouse_file_path, 'r') as wh_file:
    warehouses = json.load(wh_file)

items_file_path = decompress_file('../couchbase-server/sample-items.json.zip')
with open(items_file_path, 'r') as it_file:
    items = json.load(it_file)

districts_file_path = decompress_file('../couchbase-server/sample-districts.json.zip')
with open(districts_file_path, 'r') as dt_file:
    districts = json.load(dt_file)

# Create a mapping of warehouse ID to its districts
warehouse_to_districts = {}
for district in districts:
    warehouse_id = district["warehouseId"]
    if warehouse_id not in warehouse_to_districts:
        warehouse_to_districts[warehouse_id] = []
    warehouse_to_districts[warehouse_id].append(district["districtId"])


# Function to generate stock data for each warehouse with each item
def generate_stock_data(warehouses, items, warehouse_to_districts):
    stock_data = []

    for warehouse in warehouses:
        warehouse_id = warehouse["warehouseId"]
        district_ids = warehouse_to_districts.get(warehouse_id, [])

        for item in items:
            item_id = item["itemId"]

            stock_entry = {
                "itemId": item_id,
                "warehouseId": warehouse_id,
                "quantity": randint(1, 10000),  # Random stock quantity between 1 and 100
                "district01": district_ids[0] if len(district_ids) > 0 else "",  # Use district ID if available
                "district02": district_ids[1] if len(district_ids) > 1 else "",
                "district03": district_ids[2] if len(district_ids) > 2 else "",
                "district04": district_ids[3] if len(district_ids) > 3 else "",
                "district05": district_ids[4] if len(district_ids) > 4 else "",
                "district06": district_ids[5] if len(district_ids) > 5 else "",
                "district07": district_ids[6] if len(district_ids) > 6 else "",
                "district08": district_ids[7] if len(district_ids) > 7 else "",
                "district09": district_ids[8] if len(district_ids) > 8 else "",
                "district10": district_ids[9] if len(district_ids) > 9 else "",
                "salesYtd": 0,  # Initialize year-to-date sales to 0
                "salesOrderCount": 0,  # Initialize order count to 0
                "salesRemoteOrderCount": 0,  # Initialize remote order count to 0
                "data": f"Stock data for {item['name']} in {warehouse['name']}"
            }

            stock_data.append(stock_entry)

    return stock_data


# Generate stock data
stock_data = generate_stock_data(warehouses, items, warehouse_to_districts)

# Save the stock data to a new JSON file
with open('../couchbase-server/sample-stock.json', 'w') as stock_file:
    json.dump(stock_data, stock_file, indent=4)

print("Stock data has been generated and saved to stock.json")
