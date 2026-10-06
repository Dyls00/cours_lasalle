import json

files_to_update = [
    '/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/08_capstone_eda_thelook.ipynb',
    '/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/solutions/08_capstone_eda_thelook_solution.ipynb'
]

for file_path in files_to_update:
    try:
        with open(file_path, 'r') as f:
            nb = json.load(f)
        
        new_cells = []
        for cell in nb['cells']:
            src_str = ''.join(cell['source'])
            
            # Remove the cell if it's the NumPy challenge
            if "# 3. Défi NumPy" in src_str:
                continue
                
            # Update the markdown title for Part 1
            if "## 🛠️ PARTIE 1 : Chargement & Exploration Initiale" in src_str:
                cell['source'] = [
                    "---\n",
                    "## 🛠️ PARTIE 1 : Chargement & Exploration Initiale (Pandas)\n",
                    "*Valide les compétences du Notebook 2 (Pandas Premiers Pas).*"
                ]
                
            new_cells.append(cell)
            
        nb['cells'] = new_cells
        
        with open(file_path, 'w') as f:
            json.dump(nb, f, indent=1)
            
        print(f"Successfully updated {file_path}")
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}")

