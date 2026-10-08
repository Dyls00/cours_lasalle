import json

file_path = "big_data/02_cours/day2_transformation/labs/01_lab_medallion_bases.ipynb"
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells in Lab 1: {len(nb['cells'])}")
