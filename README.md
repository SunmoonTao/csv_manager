
# CSV Manager

A simple Python package for managing CSV files like a database, allowing for querying, adding, updating, and saving changes.

## Installation

You can install the package using pip:

```bash
pip install ./csv_manager
```

Alternatively, if you have the package source code, navigate to the `csv_manager` directory (the one containing `setup.py`) and run:

```bash
pip install .
```

## Usage

Here's how to use the `CSVManager` class:

```python
import pandas as pd
import os
from csv_manager.manager import CSVManager # Assuming the class is in manager.py

# Create a dummy CSV file for demonstration (if it doesn't exist)
csv_filename = "my_data.csv"
if not os.path.exists(csv_filename):
    initial_data = {
        'ID': [1, 2, 3, 4, 5],
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 28, 40],
        'City': ['NY', 'LA', 'NY', 'SF', 'LA'],
        'Status': ['Active', 'Pending', 'Active', 'Active', 'Pending']
    }
    initial_df = pd.DataFrame(initial_data)
    initial_df.to_csv(csv_filename, index=False)
    print(f"Created initial '{csv_filename}'")
else:
    print(f"'{csv_filename}' already exists, using existing file.")


# Initialize the CSVManager
# You can specify 'ID' as an index column if it's unique and you want to use it
# manager = CSVManager(csv_filename, index_col='ID')
manager = CSVManager(csv_filename) # Using default integer index for simplicity

print("--- Current Data ---")
print(manager.data)

# Querying data
print("
--- Query: People older than 30 ---")
older_people = manager.query(condition_func=lambda row: row['Age'] > 30)
print(older_people)

# Adding a new row
print("
--- Adding new row ---")
new_entry = {'ID': 6, 'Name': 'Frank', 'Age': 22, 'City': 'Chicago', 'Status': 'Active'}
manager.add_row(new_entry)
print(manager.data)

# Updating data
print("
--- Updating Status to 'Completed' for 'Pending' entries ---")
manager.update_data(
    condition_func=lambda row: row['Status'] == 'Pending',
    updates={'Status': 'Completed', 'Age': lambda row: row['Age'] + 1}
)
print(manager.data)

# Deleting data
print("
--- Deleting rows for people in LA ---")
manager.delete_rows(condition_func=lambda row: row['City'] == 'LA')
print(manager.data)

# Save all changes back to the CSV
print("
--- Saving Changes ---")
manager.save_changes(index=False) # index=False prevents writing the pandas DataFrame index as a column

# Verify changes by reloading the CSV (optional)
print("
--- Verifying saved changes by reloading the CSV ---")
reloaded_df = pd.read_csv(csv_filename)
print(reloaded_df)

# Clean up the dummy CSV file (optional)
# os.remove(csv_filename)
# print(f"
Cleaned up: '{csv_filename}' removed.")

