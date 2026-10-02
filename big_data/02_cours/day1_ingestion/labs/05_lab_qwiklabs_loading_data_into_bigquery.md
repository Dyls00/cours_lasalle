# 🧪 TP Google Lab : Loading Data into BigQuery
*(Inspiré du lab officiel Google Cloud Skills Boost : "Loading Data into BigQuery")*

---

## 🎯 Objectifs du Lab
1. Créer un dataset BigQuery personnalisé.
2. Charger des données tabulaires **CSV** avec autodétection de schéma (`--autodetect`).
3. Charger des données semi-structurées **JSONL (Newline Delimited JSON)** en définissant un schéma JSON strict.
4. Exécuter des requêtes de validation pour vérifier les lignes chargées.

---

## 📋 Tâche 1 : Création du Dataset
Dans Cloud Shell ou l'éditeur SQL BigQuery :

```bash
export PROJECT_ID=$(gcloud config get-value project)

# Créer le dataset e-commerce dans la région EU
bq mk --location=EU --dataset "${PROJECT_ID}:ecommerce"
```

---

## 📋 Tâche 2 : Chargement d'un fichier CSV (Autodétection)
Nous allons charger des données de transactions CSV hébergées dans un bucket GCS.

```bash
# Chargement du fichier CSV d'exemple
bq load \
    --source_format=CSV \
    --autodetect \
    --skip_leading_rows=1 \
    "${PROJECT_ID}:ecommerce.transactions_csv" \
    gs://cloud-training/gcpbu/transactions.csv
```

Vérification du schéma généré automatiquement :
```bash
bq show --schema --format=prettyjson "${PROJECT_ID}:ecommerce.transactions_csv"
```

---

## 📋 Tâche 3 : Chargement d'un fichier JSONL avec schéma explicite
Pour les fichiers JSON contenant des structures imbriquées, il est recommandé de fournir le schéma au format JSON pour éviter les erreurs de typage.

1. **Définition du fichier de schéma (`schema.json`)** :
```json
[
  {"name": "order_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "customer_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "transaction_date", "type": "DATE", "mode": "NULLABLE"},
  {"name": "total_amount", "type": "FLOAT", "mode": "NULLABLE"}
]
```

2. **Commande de chargement `bq load`** :
```bash
bq load \
    --source_format=NEWLINE_DELIMITED_JSON \
    "${PROJECT_ID}:ecommerce.orders_json" \
    gs://cloud-training/gcpbu/orders.json \
    ./schema.json
```

---

## 📋 Tâche 4 : Validation SQL
Exécutez dans l'interface BigQuery :

```sql
SELECT
  COUNT(1) AS total_orders,
  ROUND(SUM(total_amount), 2) AS total_revenue
FROM
  `ecommerce.orders_json`;
```

---

## ✅ Checkpoint d'évaluation (Style Qwiklabs)
- [ ] Dataset `ecommerce` créé en région `EU`.
- [ ] Table `transactions_csv` créée avec l'option `--autodetect`.
- [ ] Table `orders_json` chargée avec le fichier de schéma explicite.
