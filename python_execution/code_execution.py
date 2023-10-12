import pandas as pd
from pathlib import Path
from json_csv_compare.config import cfg 

# Read the JSON file
path_json = Path(r"C:/Users/Sayalee/Downloads/EmployeeData.json")

data = pd.read_json(path_json)

# Save the data as CSV
load_csv = cfg.path_excel / "{file.stem}.csv"

data.to_csv(load_csv, index=False)

print('CSV file saved successfully.')