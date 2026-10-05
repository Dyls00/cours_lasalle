# 🎓 Examen Pratique & Évaluation Finale : Data Engineer chez "TheLook Global"

**Formation :** Introduction au Big Data
**Durée de l'épreuve :** 2h30  
**Modalité :** Projet individuel noté sur 20 points  
**Livrable :** Dépôt GitHub propre contenant le code, les requêtes SQL, le workflow CI/CD et le QCM rempli  

---

## 📌 1. Contexte Métier & Enjeux

Vous venez d'intégrer en tant que **Data Engineer** la scale-up e-commerce **TheLook Global** (500 000 clients actifs). 

Pour optimiser sa politique commerciale et détecter les tendances d'achat, l'équipe produit a mis en place une API REST exposant les flux de paniers et de commandes en temps réel. Cependant, les données brutes sont hétérogènes (JSON imbriqué, formats de dates variés, doublons réseau, anomalies de typage).

Votre mission consiste à **concevoir, implémenter et automatiser de bout en bout un pipeline de données moderne (ELT)** répondant aux exigences du Big Data :
1. **Ingestion brute & découplée** dans le Cloud (couche Bronze) avec `dlt`.
2. **Transformations et modélisation analytique** (couches Silver & Gold) dans BigQuery, en exploitant le stockage colonnaire, la déduplication par Window Functions et le partitionnement.
3. **Automatisation et orchestration Serverless** via un DAG GitHub Actions respectant les bonnes pratiques FinOps et de sécurité.

---

## 🏛️ 2. Architecture Cible du Pipeline

```
  [ Source API ] : FakeStore API (/carts & /products)
         │
         │  1. Ingestion ELT Python (dlt)
         ▼
  ┌────────────────────────────────────────────────────────┐
  │ 🥉 Couche BRONZE (BigQuery : raw_events / raw_carts)   │
  │    - Données JSON brutes, jamais altérées              │
  │    - Métadonnées d'audit (_dlt_load_id, timestamp)     │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             │  2. Transformations SQL & Typage
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 🥈 Couche SILVER (BigQuery : silver.orders_cleaned)     │
  │    - Typage strict (SAFE_CAST, TIMESTAMP)              │
  │    - Déduplication (ROW_NUMBER / QUALIFY)              │
  │    - Aplatissement des items imbriqués (UNNEST/ARRAY)  │
  │    - Optimisation : PARTITION BY date, CLUSTER BY id   │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             │  3. Agrégations & Modélisation
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 🥇 Couche GOLD (BigQuery : gold.daily_kpis / Marts)    │
  │    - Table dénormalisée / Vue Matérialisée             │
  │    - KPIs métier (CA, panier moyen, volumes)           │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             │  4. Automatisation & Qualité
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ ⚙️ Orchestration CI/CD & Contrôle Qualité             │
  │    - GitHub Actions (cron nightly + workflow_dispatch) │
  │    - Tests d'intégrité (dbt test / assertions SQL)     │
  │    - Requête analytique finale (Top Catégories)        │
  └────────────────────────────────────────────────────────┘
```

---

## 🎯 3. Jalons & Travail Demandé (Barème sur 20 points)

Le sujet est structuré en **4 jalons interdépendants**, chacun noté sur 5 points.

```
┌────────────────────────────────────────────────────────────────────────┐
│  Jalon 1 : QCM Théorique & Architecture Cloud             ──►  5 pts   │
│  Jalon 2 : Ingestion ELT & Couche Bronze (dlt)            ──►  5 pts   │
│  Jalon 3 : Transformations Medallion (Silver & Gold SQL)  ──►  5 pts   │
│  Jalon 4 : Qualité, Orchestration Serverless & Analytics  ──►  5 pts   │
│                                                                        │
│  TOTAL                                                    ──► 20 pts   │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 📝 Jalon 1 — QCM Théorique & Fondamentaux Big Data (5 points)


Ce questionnaire de 10 questions (0.5 pt par question) valide votre compréhension des piliers du cours :
- Les **5 V du Big Data** et le passage historique de l'ETL vers l'**ELT**.
- Les différences fondamentales entre **OLTP (lignes)** et **OLAP (stockage colonnaire)**.
- Le **découplage Stockage / Calcul** et les mécanismes de facturation FinOps sur BigQuery.
- L'**Architecture Medallion** (rôles respectifs de Bronze, Silver, Gold).
- La modélisation **Dénormalisée (`STRUCT` / `ARRAY`)** vs le modèle en étoile (Kimball).
- La distinction entre **Vue Logique** et **Vue Matérialisée** (Materialized View).
- Les principes de l'**Orchestration par DAG** et de l'**abstraction Serverless** (FaaS / CI/CD).

---

### 📥 Jalon 2 — Ingestion ELT vers la Couche Bronze avec `dlt` (5 points)

Vous devez développer un script Python exécutable autonome nommé `ingestion/pipeline_bronze.py` qui extrait les données depuis l'API FakeStore et les ingère dans BigQuery.

#### Spécifications techniques :
1. **Source de données :**
   - Endpoint des paniers : `https://fakestoreapi.com/carts`
   - *(Optionnel / Bonus)* Endpoint des produits pour enrichissement : `https://fakestoreapi.com/products`
2. **Destination BigQuery :**
   - Dataset cible : `bronze`
   - Table cible : `bronze.raw_carts` (ou tables générées par le schéma dlt).
3. **Exigences du script :**
   - Utiliser la bibliothèque `dlt` (`dlt.pipeline(...)`).
   - Déclarer une ressource `@dlt.resource` extrayant les données au format générateur Python (`yield`).
   - Conserver l'intégralité de la donnée brute sans filtrage destructif (principe de la couche Bronze).
   - Configurer le mode de chargement adéquat (`write_disposition="replace"` pour le développement ou `"append"` pour un flux continu).
   - Assurer la traçabilité de l'ingestion (présence automatique des métadonnées `_dlt_load_id`, `_dlt_id`).

#### Critères d'évaluation du Jalon 2 :
- [ ] Initialisation et exécution sans erreur du pipeline `dlt` vers BigQuery *(2 pts)*.
- [ ] Conception propre de la ressource/source dlt avec fonction génératrice *(1.5 pt)*.
- [ ] Respect des principes de la couche Bronze (conservation du brut, métadonnées d'audit) *(1 pt)*.
- [ ] Propreté du code, modularité et gestion des exceptions HTTP *(0.5 pt)*.

---

### 🔄 Jalon 3 — Modélisation Medallion : Couches Silver & Gold (5 points)

À partir des données brutes chargées dans `bronze`, concevez les requêtes SQL (ou modèles `dbt`) assurant le raffinement de la donnée. Vous enregistrerez vos requêtes dans le dossier `transformations/`.

#### 1. Couche Silver (`transformations/01_silver_orders.sql`) — 3 points
Créez ou remplacez la table `silver.orders_cleaned` :
- **Typage strict & sécurisé** : convertir les dates textuelles en `TIMESTAMP` ou `DATE` (`PARSE_TIMESTAMP` ou `TIMESTAMP()`), convertir les montants et identifiants avec `SAFE_CAST`.
- **Aplatissement (Unnesting)** : la structure source contient une liste d'articles imbriqués (`products`). Utilisez `UNNEST` (ou les tables dérivées générées par `dlt`) pour extraire chaque article avec sa quantité (`quantity`) et son `productId`.
- **Déduplication robuste** : appliquer la Window Function `ROW_NUMBER() OVER (PARTITION BY cart_id, product_id ORDER BY date DESC)` (ou clause `QUALIFY`) pour éliminer d'éventuels doublons d'événements.
- **Filtrage de qualité** : exclure les quantités négatives ou nulles et les enregistrements sans date valide.
- **Optimisation FinOps (BigQuery)** :
  - `PARTITION BY DATE(order_date)` pour limiter le volume scanné lors des requêtes temporelles.
  - `CLUSTER BY user_id` (ou `product_id`) pour accélérer les jointures et filtres récurrents.

#### 2. Couche Gold (`transformations/02_gold_kpis.sql`) — 2 points
Créez la table ou vue matérialisée `gold.daily_kpis` :
- Agréger les données par date (`report_date`) :
  - Nombre total de commandes / paniers validés (`COUNT(DISTINCT cart_id)`).
  - Nombre total d'articles vendus (`SUM(quantity)`).
  - Nombre de clients distincts actifs (`COUNT(DISTINCT user_id)`).
  - Quantité moyenne d'articles par commande (`avg_basket_size`).
- **Choix architectural argumenté** : justifiez en commentaire SQL pourquoi vous avez opté pour une **Table partitionnée planifiée** ou pour une **Vue Matérialisée** (`CREATE MATERIALIZED VIEW`) au regard des contraintes de rafraîchissement et de coût.

#### Critères d'évaluation du Jalon 3 :
- [ ] Typage robuste, filtrage des anomalies et déduplication par Window Function (`ROW_NUMBER`) *(1.5 pt)*.
- [ ] Dépliage correct des structures imbriquées (`ARRAY` / `STRUCT` / `UNNEST`) *(1 pt)*.
- [ ] Mise en œuvre prouvée du `PARTITION BY` et `CLUSTER BY` *(1 pt)*.
- [ ] Table/Vue Gold exacte avec KPIs agrégés cohérents *(1 pt)*.
- [ ] Rigueur de la syntaxe SQL et justification architecturale claire *(0.5 pt)*.

---

### ⚙️ Jalon 4 — Qualité des Données, Orchestration CI/CD & Requête Analytique (5 points)

#### 1. Contrôle de Qualité des Données (1.5 point)
Dans un fichier `transformations/tests_qualite.sql` (ou via les tests `dbt` dans `schema.yml`) :
- Implémentez au moins **3 assertions de qualité** vérifiant la fiabilité de la couche Silver / Gold :
  1. **Unicité** de la clé primaire composite (`cart_id` + `product_id`).
  2. **Non-nullité** des colonnes critiques (`order_date`, `user_id`, `quantity`).
  3. **Règle métier de positivité** (`quantity > 0`).

#### 2. Orchestration Serverless CI/CD (2 points)
Créez le fichier de workflow GitHub Actions `.github/workflows/data_pipeline.yml` :
- Modélisez le pipeline sous la forme d'un **DAG séquentiel** :
  1. *Step 1* : Checkout du code & configuration de l'environnement Python.
  2. *Step 2* : Authentification sécurisée à Google Cloud via secret GitHub (`GCP_SA_KEY` ou `GCP_CREDENTIALS_JSON`).
  3. *Step 3* : Exécution de l'ingestion `dlt` (Couche Bronze).
  4. *Step 4* : Exécution des transformations Silver & Gold.
  5. *Step 5* : Exécution des tests de qualité (le pipeline doit échouer si un test de qualité est rouge).
- Configurez un déclenchement automatique planifié (`schedule: - cron: '0 3 * * *'`) ainsi qu'un déclenchement manuel (`workflow_dispatch`).
- **Sécurité absolue** : aucune clé de compte de service ou mot de passe ne doit être écrit en clair dans le code.

#### 3. Requête Analytique Finale & FinOps (1.5 point)
Dans un fichier `transformations/03_analytique_top_categories.sql` :
- Rédigez une requête SQL analytique qui exploite les données consolidées pour répondre à la direction :
  - Calculer pour chaque mois le classement des utilisateurs les plus actifs (ou produits les plus vendus) en utilisant une Window Function de classement (`RANK() OVER(...)` ou `DENSE_RANK() OVER(...)`).
  - Sélectionner uniquement le **Top 3** de chaque période.
- **Analyse FinOps en commentaire** :
  - Expliquez comment vérifier le nombre d'octets scannés avant exécution (*Dry Run* dans l'UI BigQuery ou flag `--dry_run` du CLI `bq`).
  - Justifiez pourquoi cette requête est plus économique sur BigQuery qu'un `SELECT *` sur une base OLTP traditionnelle.

---

## 📂 4. Structure Attendue du Dépôt

Votre rendu final sur GitHub doit présenter l'arborescence suivante :

```
examen-big-data-thelook/
├── .github/
│   └── workflows/
│       └── data_pipeline.yml          # Workflow d'orchestration CI/CD (Jalon 4)
├── ingestion/
│   └── pipeline_bronze.py             # Script d'ingestion dlt vers BigQuery (Jalon 2)
├── transformations/
│   ├── 01_silver_orders.sql           # Typage, UNNEST, déduplication, partition (Jalon 3)
│   ├── 02_gold_kpis.sql               # Data mart / Vue matérialisée des KPIs (Jalon 3)
│   ├── 03_analytique_top_categories.sql# Window Function analytique & FinOps (Jalon 4)
│   └── tests_qualite.sql              # Assertions / Tests dbt de qualité (Jalon 4)
├── pyproject.toml                     # Dépendances du projet (ou requirements.txt)
├── qcm_theorique.md                   # Réponses complètes aux 10 questions (Jalon 1)
└── README.md                          # Documentation synthétique d'exécution
```

---

## 📊 5. Grille d'Évaluation Récapitulative (/20)

| Jalon | Intitulé | Points | Critères d'Excellence |
|:---:|:---|:---:|:---|
| **1** | **QCM Théorique & Architecture** | **/5** | Exactitude des réponses sur les concepts clés (5 V, ELT, colonnaire, Medallion, DAG, Serverless). |
| **2** | **Ingestion ELT (dlt)** | **/5** | Pipeline dlt fonctionnel vers BigQuery `bronze`, conservation intégrale du brut, traçabilité et propreté du code. |
| **3** | **Transformations Silver & Gold** | **/5** | Typage `SAFE_CAST`, déduplication `ROW_NUMBER`, aplatissement `UNNEST`, `PARTITION BY` + `CLUSTER BY`, Data Mart Gold. |
| **4** | **Qualité, Orchestration & Analytics** | **/5** | Tests de données stricts, workflow GitHub Actions (DAG + secrets), requête analytique Window Function et justification FinOps. |
| **TOTAL** | **Note Finale** | **/20** | **Validation des compétences Data Engineer Big Data sur GCP.** |

---

## 📬 6. Consignes de Rendu

1. Vérifiez que votre code fonctionne de bout en bout et qu'**aucun secret GCP (`.json`) n'a été committé dans Git** (pensez à vérifier votre `.gitignore`).
2. Faites un `git push` de l'ensemble de votre travail sur votre dépôt GitHub personnel.
3. Déposez l'URL de votre dépôt GitHub sur la plateforme pédagogique avant la fin du temps imparti (2h30).
