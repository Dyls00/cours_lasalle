import json

file_path = '/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/solutions/08_capstone_eda_thelook_solution.ipynb'
try:
    with open(file_path, 'r') as f:
        nb = json.load(f)
    
    for cell in nb['cells']:
        src = cell['source']
        if isinstance(src, list):
            cell['source'] = [line.replace("../01_data/", "../../01_data/") for line in src]
            
    with open(file_path, 'w') as f:
        json.dump(nb, f, indent=1)
    print("Fixed paths in solution notebook.")
except Exception as e:
    print(f"Error: {e}")
