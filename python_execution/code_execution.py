import pandas as pd
from pathlib import Path
from json_csv_compare.config import cfg 
from json_csv_compare.log_factory import logger


# Read the JSON file
import json


path_json = Path(r"C:/Users/Sayalee/Downloads/EmployeeData.json")
with open(path_json, 'r') as f:
    data = json.load(f)

data_normalized = df = pd.json_normalize(data)

logger.info(data)
# Save the data as CSV
load_csv = cfg.path_csv / f"{path_json.stem}.csv"

data_normalized.to_csv(load_csv, index=False)

print('CSV file saved successfully at')