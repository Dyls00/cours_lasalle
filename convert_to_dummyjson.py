import json

file_path = "big_data/02_cours/day1_ingestion/bonus/02_ingestion_dlt_sources_and_resources.ipynb"
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get("cells", []):
    if cell["cell_type"] == "markdown":
        new_source = []
        for line in cell["source"]:
            line = line.replace("FakeStore API", "DummyJSON API")
            line = line.replace("FakeStore", "DummyJSON")
            line = line.replace("fakestoreapi.com", "dummyjson.com")
            line = line.replace('rating: {"rate": 4.1, "count": 259}', 'dimensions: {"width": 28.01, "height": 14.38, "depth": 27.71}')
            line = line.replace("rating__rate", "dimensions__width")
            line = line.replace("rating__count", "dimensions__height")
            line = line.replace('"date": "2020-03-02T00:00:00.000Z",', '"totalProducts": 5,')
            line = line.replace('{"productId": 1, "quantity": 4}', '{"id": 59, "quantity": 1}')
            line = line.replace('{"productId": 5, "quantity": 1}', '{"id": 88, "quantity": 2}')
            line = line.replace("address__geolocation__lat", "address__coordinates__lat")
            line = line.replace("name__firstname", "firstName")
            line = line.replace("name__lastname", "lastName")
            line = line.replace("fakestore", "dummyjson")
            
            new_source.append(line)
        cell["source"] = new_source
        
    elif cell["cell_type"] == "code":
        new_source = []
        code_str = "".join(cell["source"])
        for line in cell["source"]:
            # URL replacements
            line = line.replace("fakestoreapi.com", "dummyjson.com")
            line = line.replace("FakeStore", "DummyJSON")
            line = line.replace("fakestore", "dummyjson")
            
            # extract correct keys from JSON
            if "products = response.json()" in line:
                line = line.replace("response.json()", "response.json()['products']")
            elif "carts = response.json()" in line:
                line = line.replace("response.json()", "response.json()['carts']")
            elif "yield response.json()" in line and "get_carts_without_subtables" in code_str:
                line = line.replace("response.json()", "response.json()['carts']")
            elif "yield response.json()" in line and "get_ecommerce_users" in code_str:
                line = line.replace("response.json()", "response.json()['users']")
                
            # Columns selections
            line = line.replace("'rating__rate', 'rating__count'", "'dimensions__width', 'dimensions__height'")
            line = line.replace("'name__firstname', 'name__lastname'", "'firstName', 'lastName'")
            line = line.replace("'address__geolocation__lat'", "'address__coordinates__lat'")
            
            # SQL replacements
            if "c.date," in line:
                continue # Remove this line
            if "cp.product_id" in line:
                line = line.replace("cp.product_id", "cp.id AS product_id")
            
            new_source.append(line)
        cell["source"] = new_source

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write("\n")

print("Notebook converted to DummyJSON successfully!")
