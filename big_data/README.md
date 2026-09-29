# 🚀 Formation Intensive : Initiation au Big Data & Data Engineering sur GCP (21h)

Bienvenue dans le dépôt du cours **Initiation au Big Data & Data Engineering** (3 jours / 21h).

Cette formation est axée à **80% sur la pratique** et s'appuie sur l'écosystème **Google Cloud Platform (GCP)**, les labs officiels **Google Cloud Skills Boost / Qwiklabs**, et des outils modernes de Data Engineering (**BigQuery, dlt, dbt, Apache Beam, Dataflow, Looker Studio**).

---

## 📅 Programme du Cours, Slides & Labs Qwiklabs

### 🟢 Jour 1 : Comprendre, stocker, ingérer (7h)

| Module | Durée | Type | Supports & Contenu |
| :--- | :---: | :---: | :--- |
| **1.1 Le paradigme Big Data** | 1h15 | Théorie + Démo | 📊 [Slides Théo 1.1](02_labs/slides/01_slides_paradigme_bigdata.md)<br>Les 5V, OLTP vs OLAP, calcul distribué, découplage stockage/calcul, Lake / DWH / Lakehouse. |
| **1.2 GCP, coûts, gouvernance** | 0h45 | Mixte | Projets GCP, IAM, résidence des données en EU (RGPD), modèle de tarification BigQuery & Cloud Storage, configuration d'alertes budgétaires en direct. |
| **1.3 Prise en main BigQuery** | 0h30 | Pratique | Cloud Shell Editor / VS Code local + CLI `gcloud` & `bq`. Requêtes sur datasets publics, utilisation du **Dry Run** pour estimer le coût des requêtes. |
| **1.4 Lake vs Data Warehouse** | 1h15 | Pratique | 🧪 [Lab Qwiklabs Data Lake CLI](02_labs/day1_ingestion/04_lab_qwiklabs_data_lake_and_gcs_cli.md)<br>Création de buckets GCS, stockage de logs JSON, création de **Tables Externes**, chargement en **Tables Natives BigQuery**. |
| **1.5 ELT & Ingestion avec `dlt`** | 3h15 | Théorie (30m) + Pratique | 🧪 [Lab Qwiklabs Loading Data into BQ](02_labs/day1_ingestion/05_lab_qwiklabs_loading_data_into_bigquery.md)<br>Ingestion d'API REST vers BigQuery (Couche **Bronze**), gestion de la *schema evolution* et du chargement incrémental. |

---

### 🟡 Jour 2 : Analyser et transformer (7h)

| Module | Durée | Type | Supports & Contenu |
| :--- | :---: | :---: | :--- |
| **2.1 Performance et Coûts BigQuery** | 1h00 | Mixte | 🧪 [Lab Qwiklabs Partitioned & Clustered Tables](02_labs/day2_transformation/01_lab_qwiklabs_partitioned_clustered_tables.md)<br>**Partitionnement** (par date/ingestion) et **Clustering**. Benchmark de coût et Pruning sur le dataset StackOverflow. |
| **2.2 SQL Analytique & Semi-structuré** | 2h00 | Pratique | 🧪 [Lab Qwiklabs JSON, Arrays & Nested Data](02_labs/day2_transformation/02_lab_qwiklabs_analyzing_json_arrays_nested.md)<br>CTE, manipulation avancée de JSON/Structs/Arrays avec `UNNEST`, `STRUCT`, `ARRAY_AGG` et **Window Functions**. |
| **2.3 Modélisation & Architecture Medallion** | 0h30 | Théorie | 📊 [Slides Théo 2.3](02_labs/slides/02_slides_medallion_et_modelisation.md)<br>Modélisation d'une base analytique : Modèle en Étoile (Kimball) vs Dénormalisation BigQuery. Architecture Medallion (**Bronze, Silver, Gold**). |
| **2.4 Transformation avec `dbt`** | 3h30 | Théorie (30m) + Pratique | Initialisation d'un projet `dbt-bigquery`. Construction de la **couche Silver** (nettoyage, typage, déduplication) et de la **couche Gold** (marts & agrégats métier). |

---

### 🔴 Jour 3 : Fiabiliser, streamer, évaluer (7h)

| Module | Durée | Type | Supports & Contenu |
| :--- | :---: | :---: | :--- |
| **3.1 Qualité & Contrats de Données** | 1h00 | Mixte | Data Contracts, tests `dbt` (generic & singular), freshness des données. *Exercice : "Casser un test et réparer le pipeline".* |
| **3.2 Orchestration de Pipeline** | 0h45 | Pratique | Script d'orchestration end-to-end (Bash / GitHub Actions) enchaînant : `dlt` (ingestion) ➔ `dbt run` (transformations) ➔ `dbt test` (validation). |
| **3.3 Vélocité : Pub/Sub, Beam & Dataflow** | 2h15 | Théorie (30m) + Pratique | 📊 [Slides Théo 3.3](02_labs/slides/03_slides_streaming_pubsub_beam.md)<br>Traitement Batch vs Streaming, fenêtrage (windowing), gestion des files et doublons. Exécution d'un pipeline **Apache Beam** en local puis sur **Google Cloud Dataflow** vers BigQuery. |
| **3.4 Data Viz avec Looker Studio** | 0h30 | Pratique | Connexion directe à la table Gold BigQuery et création d'un tableau de bord décisionnel d'une page. |
| **3.5 Cas pratique évalué (Examen)** | 2h30 | Autonomie / Évaluation | **Mission globale sur dépôt Git :** Ingestion d'une API dédiée via `dlt`, aplatissement des JSON dans BigQuery, transformation dbt (Silver/Gold) documentée et testée, et requêtes analytiques finales. + QCM théorique. |

---

## 📁 Structure du Répertoire

```text
big_data/
├── 01_data/                 # Datasets bruts, schémas JSON, exemples de logs
├── 02_labs/                 # TPs, exercices et scripts guidés
│   ├── slides/              # 📊 Présentations / Slides de cours (Marp Markdown)
│   ├── day1_ingestion/      # GCP CLI, GCS Data Lake, Loading Data into BQ, dlt
│   ├── day2_transformation/ # Partitioning/Clustering, JSON/UNNEST, Projet dbt
│   └── day3_production/     # dbt tests, Orchestration, Apache Beam / Dataflow, Looker Studio
├── 03_evaluation/           # Sujet et base du Cas Pratique Évalué (Examen final)
├── pyproject.toml           # Gestion des dépendances Python (uv)
└── README.md                # Ce document
```

---

## 🛠️ Préréquis & Configuration de l'Environnement

### 1. Outils requis
- **Python 3.11+** (géré via `uv`)
- **Google Cloud SDK (`gcloud` CLI)**
- Un compte **Google Cloud Platform** (Projet GCP configuré avec facturation activée ou crédits étudiants).

### 2. Installation de l'environnement Python
```bash
cd big_data
uv sync
```
