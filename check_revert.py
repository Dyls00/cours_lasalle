import json

files_to_check = [
    '/Users/macbook/Development/cours_lasalle/big_data/02_cours/day1_ingestion/labs/03_lab_data_lake_and_external_tables.ipynb',
    '/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/05_exercice_integrateur.ipynb',
    '/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/08_capstone_eda_thelook.ipynb',
    '/Users/macbook/.gemini/antigravity/brain/4a9271e1-d123-4dc3-8e1b-a51c1b2f9524/syllabus_numpy_pandas_14h.md'
]

for p in files_to_check:
    try:
        with open(p, 'r') as f:
            content = f.read()
            print(f"--- {p} ---")
            if p.endswith('.ipynb'):
                nb = json.loads(content)
                for cell in nb['cells'][:15]:
                    src = ''.join(cell['source'])
                    if 'Option B' in src or 'Analyste Junior' in src or 'Capstone' in src:
                        print(src[:200])
            else:
                print(content[16500:17000]) # just checking a slice for the syllabus
    except Exception as e:
        print(f"Error reading {p}: {e}")

