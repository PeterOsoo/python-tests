import json
import csv
import random

# Define worker names
workers = ["John Smith", "Mabel Lee",
           "Jan Novák", "Navn Navnesen", "Zhang San"]


# Function to check if 'Type' meets the condition
def is_valid_type(type_value):
    valid_types = ["4800a", "501c", "325d"]
    return type_value in valid_types


# Function to check if 'Series' meets the condition
def is_valid_series(series_value):
    return series_value.startswith("INV") and series_value[3:].isdigit() and len(series_value) == 6


# Load input data from JSON file
with open("input.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Initialize the master data list
master_data = []

# Initialize individual worker data dictionaries
worker_data = {worker: [] for worker in workers}

# Filter and assign rows
valid_rows = []
for entry in data:
    company = entry.get("Company")
    type_value = entry.get("Type")
    series_value = entry.get("Series")

    # Check 'Type' and 'Series' conditions
    if not is_valid_type(type_value):
        status = "Incorrect Type"
        assignee = ""
    elif not is_valid_series(series_value):
        status = "Incorrect Series"
        assignee = ""
    else:
        # If both conditions are met, mark as assigned and collect the valid row
        status = "Assigned"
        valid_rows.append(entry)
        continue

    # Add entry to master data with appropriate status
    master_data.append({
        "Company": company,
        "Type": type_value,
        "Series": series_value,
        "URL": entry.get("URL", ""),
        "B2B vs B2C": entry.get("B2B vs B2C", ""),
        "Location": entry.get("Location", ""),
        "Status": status,
        "Assignee": assignee
    })

# Shuffle valid rows to ensure random assignment
random.shuffle(valid_rows)
for i, row in enumerate(valid_rows):
    # Assign rows to workers in a round-robin fashion
    assignee = workers[i % len(workers)]
    row["Assignee"] = assignee

    # Add entry to master data with assigned status
    master_data.append({
        "Company": row.get("Company"),
        "Type": row.get("Type"),
        "Series": row.get("Series"),
        "URL": row.get("URL", ""),
        "B2B vs B2C": row.get("B2B vs B2C", ""),
        "Location": row.get("Location", ""),
        "Status": "Assigned",
        "Assignee": assignee
    })

    # Add row to the corresponding worker's data
    worker_data[assignee].append({
        "Company": row.get("Company"),
        "Type": row.get("Type"),
        "Series": row.get("Series"),
        "URL": row.get("URL", ""),
        "B2B vs B2C": row.get("B2B vs B2C", ""),
        "Location": row.get("Location", "")
    })

# Write master CSV file
with open("master.csv", "w", newline="", encoding="utf-8") as master_file:
    fieldnames = ["Company", "Type", "Series", "URL",
                  "B2B vs B2C", "Location", "Status", "Assignee"]
    writer = csv.DictWriter(master_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(master_data)

# Write individual worker CSV files
for worker, rows in worker_data.items():
    filename = f"{worker.replace(' ', '_').lower()}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as worker_file:
        fieldnames = ["Company", "Type", "Series",
                      "URL", "B2B vs B2C", "Location"]
        writer = csv.DictWriter(worker_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


print("Data processing complete! Check master.csv and individual worker files.")
