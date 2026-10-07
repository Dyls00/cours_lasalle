import json

file_path = "big_data/02_cours/day1_ingestion/bonus/02_ingestion_dlt_sources_and_resources.ipynb"
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get("cells", []):
    if cell["cell_type"] == "code":
        source = cell["source"]
        new_source = []
        for line in source:
            # 1. Add curl-cffi to uv add
            if line.startswith("uv add"):
                if "curl-cffi" not in line:
                    line = line.replace("requests", "requests curl-cffi")
            
            # 2. Replace import
            if line == "from dlt.sources.helpers import requests\n":
                line = "from curl_cffi import requests\n"
            
            # 3. Replace requests.get
            if "requests.get(" in line and "impersonate" not in line:
                line = line.replace("requests.get(url)", "requests.get(url, impersonate=\"chrome\")")
                line = line.replace("requests.get(user_url)", "requests.get(user_url, impersonate=\"chrome\")")
                
            new_source.append(line)
        cell["source"] = new_source

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
    # Ensure it ends with a newline, or jupyter might complain, though json.dump doesn't add one by default

print("Notebook patched successfully!")
