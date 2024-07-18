import json
import uuid
from datetime import datetime
import random
import zipfile
import os


# Define a function to decompress a file
def decompress_file(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('../couchbase-server/')
        return os.path.splitext(file_path)[0]  # return the file path without .zip


# Load the JSON data
proj_file_path = decompress_file('../couchbase-server/sample-projects.json.zip')
with open(proj_file_path, 'r') as proj_file:
    projects = json.load(proj_file)

stock_file_path = decompress_file('../couchbase-server/sample-stock.json.zip')
with open(stock_file_path, 'r') as stock_file:
    stock_items = json.load(stock_file)

items_file_path = decompress_file('../couchbase-server/sample-items.json.zip')
with open(items_file_path, 'r') as items_file:
    items = json.load(items_file)

# Create a dictionary for quick lookup of items by itemId
items_dict = {item['itemId']: item for item in items}

# Create a dictionary for quick lookup of stock by warehouseId and itemId
stock_dict = {}
for stock in stock_items:
    if stock['warehouseId'] not in stock_dict:
        stock_dict[stock['warehouseId']] = {}
    stock_dict[stock['warehouseId']][stock['itemId']] = stock

# Initialize a dictionary to keep track of counts per warehouseId
warehouse_audit_count = {}


# Function to generate audit data for each project
def generate_audit_data(projects, stock_dict, items_dict):
    audit_data = []

    for project in projects:
        warehouse_id = project['warehouseId']
        project_id = project['projectId']
        teams = project['teams']

        # Initialize the count for this warehouseId if not already done
        if warehouse_id not in warehouse_audit_count:
            warehouse_audit_count[warehouse_id] = 0

        # Skip if this warehouse already has 1000 entries
        if warehouse_audit_count[warehouse_id] >= 1000:
            continue

        if warehouse_id in stock_dict:
            for item_id, stock in stock_dict[warehouse_id].items():
                if item_id in items_dict:
                    item = items_dict[item_id]
                    audit_entry = {
                        "auditId": str(uuid.uuid4()),
                        "isActive": True,
                        "teams": teams,
                        "modifiedOn": datetime.now().isoformat() + 'Z',
                        "createdBy": "demo@example.com",
                        "modifiedBy": "demo@example.com",
                        "projectId": project_id,
                        "createdOn": datetime.now().isoformat() + 'Z',
                        "notes": f"Found item {item['description']} in warehouse",
                        "auditCount": random.randint(0, stock['quantity']),
                        "stockItem": {
                            "name": item['name'],
                            "description": item['description'],
                            "itemId": item['itemId'],
                            "price": item['price'],
                            "style": item['style']
                        }
                    }
                    audit_data.append(audit_entry)

                    warehouse_audit_count[warehouse_id] += 1

                    # Break the inner loop if 1000 entries have been added for this warehouseId
                    if warehouse_audit_count[warehouse_id] >= 1000:
                        break
    return audit_data


# Generate audit data
audit_data = generate_audit_data(projects, stock_dict, items_dict)

# Save the audit data to a new JSON file
with open('../couchbase-server/sample-audit-inventory.json', 'w') as audit_file:
    json.dump(audit_data, audit_file, indent=4)

print("Audit data has been generated and saved to inventory.json")
