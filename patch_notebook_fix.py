import json

file_path = "big_data/02_cours/day1_ingestion/bonus/02_ingestion_dlt_sources_and_resources.ipynb"
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write("\n")

print("Notebook patched correctly with ensure_ascii=False!")
