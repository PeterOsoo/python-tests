import json
import random

# Define worker names
workers = ["John Smith", "Mabel Lee",
           "Jan Novák", "Navn Navnesen", "Zhang San"]

# Function to check data validity


def is_valid_row(row):
    type_valid = row["Type"] in ["4800a", "501c", "325d"]
    series_valid = row["Series"].startswith(
        "INV") and len(row["Series"][3:]) == 3
    return type_valid and series_valid


# Read input data
with open("data.json", "r") as f:
    data = json.load(f)

# Filter valid rows
valid_data = [row for row in data if is_valid_row(row)]

# Assign rows randomly and equally
assigned_data = {}
for worker in workers:
    assigned_data[worker] = []

# Assign rows one by one, prioritizing equal distribution
random.shuffle(valid_data)
for row in valid_data:
    min_assignments = min(len(assigned_data[worker]) for worker in workers)
    for worker, assignments in assigned_data.items():
        if len(assignments) == min_assignments:
            assignments.append(row)
            break

# Create master CSV data
master_data = []
for row in data:
    status = "Assigned" if is_valid_row(row) else (
        "Incorrect Type" if not (
            row["Type"] in ["4800a", "501c", "325d"]) else "Incorrect Series"
    )
    assignee = next(
        (w for w, assignments in assigned_data.items() if row in assignments), "")
    master_data.append({"Company": row["Company"], "Type": row["Type"], "Series": row["Series"], "URL": row["URL"],
                       "B2B vs B2C": row["B2B vs B2C"], "Location": row["Location"], "Status": status, "Assignee": assignee})

# Create individual worker CSV data
for worker, assignments in assigned_data.items():
    worker_data = [
        {k: row[k] for k in row.keys()} for row in assignments
    ]
    with open(f"{worker}.csv", "w", newline="") as f:
        fieldnames = list(worker_data[0].keys())
        from csv import DictWriter
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(worker_data)

# Create master CSV file
with open("master.csv", "w", newline="") as f:
    fieldnames = list(master_data[0].keys())
    from csv import DictWriter
    writer = DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(master_data)

print("Data processing complete! Check master.csv and individual worker files.")
