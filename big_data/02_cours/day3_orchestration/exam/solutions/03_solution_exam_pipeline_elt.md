# 🎯 Solution : Examen Final — Pipeline ELT Complet

Voici les corrections pour les différents fichiers attendus dans le dépôt GitHub.

### 1. `ingestion/load_products.py`

```python
import dlt
import requests

DATA_URL = "https://storage.googleapis.com/lasalle-public-data/messy_products.json"

def get_messy_products():
    """Récupère les données JSON depuis l'URL"""
    response = requests.get(DATA_URL)
    return response.json()

# 1. Initialisation du pipeline dlt
pipeline = dlt.pipeline(
    pipeline_name="exam_pipeline",
    destination="bigquery",       
    dataset_name="thelook_prenom" 
)

# 2. Exécution du chargement
load_info = pipeline.run(
    get_messy_products(), 
    table_name="bronze_products", 
    write_disposition="replace" 
)

print("✅ Chargement terminé !")
print(load_info)
```

---

### 2. `transformations/silver.sql`

```sql
CREATE OR REPLACE TABLE `votre_projet.thelook_prenom.silver_products` AS
SELECT
    -- 1. product_id en INT64
    SAFE_CAST(product_id AS INT64) AS product_id,
    
    -- Nom conservé tel quel
    name,
    
    -- 2. category sans null et en majuscules
    UPPER(COALESCE(category, 'UNKNOWN')) AS category,
    
    -- 3. retail_price en FLOAT64 (nettoyage du $, gestion du NA via SAFE_CAST qui renverra null)
    SAFE_CAST(REPLACE(retail_price, '$', '') AS FLOAT64) AS retail_price,
    
    -- 4. cost en FLOAT64 (transformation du mot 'NULL' en vrai null SQL)
    SAFE_CAST(NULLIF(cost, 'NULL') AS FLOAT64) AS cost,
    
    -- 5. is_active transformé en vrai BOOL
    CASE WHEN is_active = 'true' THEN TRUE ELSE FALSE END AS is_active,
    
    -- Optionnel : cast de la date si présente
    SAFE_CAST(added_date AS DATE) AS added_date
FROM
    `votre_projet.thelook_prenom.bronze_products`;
```

---

### 3. `transformations/gold.sql`

```sql
CREATE OR REPLACE TABLE `votre_projet.thelook_prenom.gold_category_metrics` AS
SELECT
    category,
    COUNT(product_id) AS total_products,
    ROUND(AVG(retail_price), 2) AS avg_retail_price,
    ROUND(AVG(retail_price - cost), 2) AS avg_margin
FROM
    `votre_projet.thelook_prenom.silver_products`
GROUP BY
    category
ORDER BY
    avg_margin DESC;
```

---

### 4. `.github/workflows/elt_pipeline.yml`

```yaml
name: Pipeline ELT Quotidien

on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'

jobs:
  run-elt:
    runs-on: ubuntu-latest
    permissions:
      contents: 'read'
      id-token: 'write'

    steps:
      - name: 📥 Récupérer le code (Checkout)
        uses: actions/checkout@v4

      - name: 🔐 Authentification Google Cloud (WIF)
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/VOTRE_NUMERO_PROJET/locations/global/workloadIdentityPools/github-pool/providers/github-provider'
          service_account: 'votre-service-account@VOTRE_PROJET.iam.gserviceaccount.com'

      - name: 🐍 Installation de Python et dlt
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: |
          pip install dlt[bigquery] requests

      - name: 1️⃣ Ingestion API vers Bronze
        run: python ingestion/load_products.py

      - name: 2️⃣ Transformation Bronze vers Silver
        run: bq query --use_legacy_sql=false < transformations/silver.sql

      - name: 3️⃣ Agrégation Silver vers Gold
        run: bq query --use_legacy_sql=false < transformations/gold.sql
```
