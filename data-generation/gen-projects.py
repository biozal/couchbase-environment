import json
import uuid
from datetime import datetime, timedelta
import random
import zipfile
import os


# Define a function to decompress a file
def decompress_file(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('../couchbase-server/')
        return os.path.splitext(file_path)[0]  # return the file path without .zip


# Load the warehouse data from the JSON file
warehouse_file_path = decompress_file('../couchbase-server/sample-warehouses.json.zip')
with open(warehouse_file_path, 'r') as wh_file:
    warehouses = json.load(wh_file)


# Function to generate a random due date at least 90 days from the current date
def generate_due_date():
    current_date = datetime.now()
    future_date = current_date + timedelta(days=random.randint(90, 365))
    return future_date.isoformat() + 'Z'


# Function to generate project data for each warehouse
def generate_project_data(warehouses):
    project_data = []
    for i, warehouse in enumerate(warehouses):
        due_date = generate_due_date()
        due_date_for_description = datetime.fromisoformat(due_date.rstrip('Z')).strftime('%Y-%m-%d')
        project = {
            "name": f"{warehouse['name']} Audit",
            "modifiedOn": datetime.now().isoformat() + 'Z',
            "createdBy": "demo@example.com",
            "dueDate": due_date,
            "description": f"Quarterly audit for the {warehouse['name']} due on {due_date_for_description}",
            "warehouseId": warehouse["warehouseId"],
            "modifiedBy": "demo@example.com",
            "teams": warehouse["shippingTo"],
            "createdOn": datetime.now().isoformat() + 'Z',
            "projectId": str(uuid.uuid4()),
            "isActive": True,
            "isComplete": False
        }
        project_data.append(project)
    return project_data


# Generate project data
projects = generate_project_data(warehouses)

# Save the project data to a new JSON file
with open('../couchbase-server/sample-projects.json', 'w') as proj_file:
    json.dump(projects, proj_file, indent=4)

print("Project data has been generated and saved to projects.json")
