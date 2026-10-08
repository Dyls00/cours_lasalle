import json
import os

def create_nb(cells, filename):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"codemirror_mode": {"name": "ipython", "version": 3}, "file_extension": ".py", "mimetype": "text/x-python", "name": "python", "nbconvert_exporter": "python", "pygments_lexer": "ipython3", "version": "3.10.0"}
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [line + "\n" if i < len(text.split("\n"))-1 else line for i, line in enumerate(text.split("\n"))]}

def code(text, language="sql"):
    return {"cell_type": "code", "execution_count": None, "metadata": {"vscode": {"languageId": language}}, "outputs": [], "source": [line + "\n" if i < len(text.split("\n"))-1 else line for i, line in enumerate(text.split("\n"))]}

cells_lab1 = [
    md("# 🔄 Lab 1 : Fondations de l'Architecture Medallion\n\n**Objectifs :**\n- Créer son propre dataset (un seul par élève pour garder le projet propre)\n- Ingérer des tables issues d'un dataset public dans sa couche Bronze (préfixe `bronze_`)\n- Joindre ces tables avant transformation\n- Nettoyer et filtrer des données brutes (Bronze ➔ Silver)\n- Comprendre Vues vs Tables Matérialisées\n- Agréger des données (Silver ➔ Gold)"),
    md("## ⚠️ Règle d'or : Projet Partagé\nNous travaillons tous sur le même projet Google Cloud. **Pour ne pas polluer l'interface avec des dizaines de dossiers, vous allez créer UN SEUL dataset portant votre prénom.**\n\nVous utiliserez ensuite des **préfixes** sur vos tables pour identifier les couches Medallion (`bronze_`, `silver_`, `gold_`).\n\nExemple de dataset : `thelook_alice`\nExemple de tables : `thelook_alice.bronze_orders`, `thelook_alice.silver_clean_orders_items`."),
    md("### Étape 1 : Création de votre dataset\nVous devez créer votre dataset `thelook_prenom`.\nGoogle Cloud vous laisse le choix des armes. **Choisissez UNE des 3 méthodes ci-dessous** :"),
    md("**Option A : Via la console BigQuery (Interface Graphique)**\n1. Dans la console, cliquez sur les 3 petits points à côté du nom du projet.\n2. Sélectionnez **Créer un ensemble de données** (Create dataset).\n3. Nommez-le `thelook_prenom`, choisissez la région `EU`, et validez."),
    md("**Option B : Via une requête SQL**\nExécutez cette cellule dans BigQuery (en remplaçant `prenom`) :"),
    code("CREATE SCHEMA IF NOT EXISTS `thelook_prenom` OPTIONS(location='EU');", "sql"),
    md("**Option C : Via le Terminal (Cloud Shell / CLI `bq`)**\nExécutez ce script bash :"),
    code("export MY_NAME=\"prenom\" # Remplacer par votre prénom\nexport PROJECT_ID=$(gcloud config get-value project)\n\nbq mk --location=EU --dataset \"${PROJECT_ID}:thelook_${MY_NAME}\"\necho \"Dataset thelook_$MY_NAME créé !\"", "shellscript"),
    md("### Étape 2 : Ingérer les données brutes (Couche Bronze)\nDans une vraie architecture Medallion, la couche Bronze est une copie **exacte** (1:1) des systèmes sources. Nous allons utiliser le dataset public e-commerce de Google : `bigquery-public-data.thelook_ecommerce`.\n\nL'objectif ici est d'**ingérer (copier)** les tables `orders` et `order_items` dans VOTRE dataset, en les préfixant par `bronze_`."),
    md("### ✍️ À vous de jouer (Exercice 1 : Ingestion Bronze)\n**Consignes :**\n1. Copiez la table `orders` publique vers `thelook_prenom.bronze_orders`.\n2. Copiez la table `order_items` publique vers `thelook_prenom.bronze_order_items`."),
    code("-- Copie de la table orders\nCREATE OR REPLACE TABLE `thelook_prenom.bronze_orders` AS\nSELECT * FROM `bigquery-public-data.thelook_ecommerce.orders`;\n\n-- Copie de la table order_items\nCREATE OR REPLACE TABLE `thelook_prenom.bronze_order_items` AS\nSELECT * FROM `bigquery-public-data.thelook_ecommerce.order_items`;", "sql"),
    md("### Étape 3 : Joindre les tables sources\nMaintenant que les tables sont chez vous, regroupons-les en une seule table brute unifiée avant de commencer le nettoyage."),
    md("### ✍️ À vous de jouer (Exercice 2 : Jointure)\n**Consignes :**\n1. Créez une table `thelook_prenom.bronze_raw_orders_items`.\n2. Faites une jointure (`JOIN`) entre vos tables locales `thelook_prenom.bronze_orders` (alias `o`) et `thelook_prenom.bronze_order_items` (alias `oi`) sur la clé `order_id`.\n3. Sélectionnez les colonnes : `o.order_id`, `o.user_id`, `o.created_at`, `o.status`, `oi.id AS order_item_id`, `oi.product_id`, `oi.sale_price`."),
    code("-- Écrivez votre requête de jointure ici :\nCREATE OR REPLACE TABLE `thelook_prenom.bronze_raw_orders_items` AS\nSELECT \n  ...\n", "sql"),
    md("## Partie 1 : Transformation Bronze ➔ Silver\nDans la couche Silver, on nettoie, on type correctement les données et on filtre ce qui n'est pas pertinent.\n\n**Exemple de nettoyage (CAST, COALESCE) :**\n```sql\nSELECT \n  order_id,\n  DATE(created_at) AS date_propre,\n  COALESCE(sale_price, 0.0) AS prix_propre\nFROM `thelook_prenom.bronze_raw_orders_items`\nWHERE status IS NOT NULL;\n```"),
    md("### ✍️ À vous de jouer (Exercice 3 : Nettoyage Silver)\n**Consignes :** \n1. Créez une table `thelook_prenom.silver_clean_orders_items` à partir de `thelook_prenom.bronze_raw_orders_items`.\n2. Convertissez le timestamp `created_at` en date simple (`DATE(created_at)`) et nommez la colonne `order_date`.\n3. Gardez uniquement les commandes dont le statut (`status`) est **'Complete'** ou **'Shipped'**.\n4. Excluez les articles dont le prix (`sale_price`) est nul ou négatif."),
    code("-- Écrivez votre requête de transformation Silver ici :\nCREATE OR REPLACE TABLE `thelook_prenom.silver_clean_orders_items` AS\nSELECT\n  ...\n", "sql"),
    md("## Partie 2 : Vue ou Table Matérialisée ?\nAu lieu d'une table physique qui doit être recalculée, on peut créer une vue matérialisée pour la couche Silver, ou une vue simple pour des requêtes de préparation.\n\n**Exemple de Vue Matérialisée :**\n```sql\nCREATE MATERIALIZED VIEW `thelook_prenom.silver_mv_shipped_orders` AS\nSELECT order_id, user_id FROM `thelook_prenom.bronze_raw_orders_items` WHERE status = 'Shipped';\n```"),
    md("### ✍️ À vous de jouer (Exercice 4 : Création d'une Vue)\n**Consignes :**\nCréez une vue classique (`CREATE OR REPLACE VIEW`) nommée `thelook_prenom.silver_v_high_value_items` qui ne sélectionne que les articles de `silver_clean_orders_items` dont le `sale_price` est supérieur à 100$. Interrogez ensuite votre vue (via un `SELECT *`)."),
    code("-- Écrivez votre création de vue ici :\n\n", "sql"),
    md("## Partie 3 : Agrégation (Silver ➔ Gold)\nLa couche Gold contient les indicateurs métier, souvent hautement agrégés pour les tableaux de bord (BI).\n\n**Exemple d'agrégation :**\n```sql\nSELECT user_id, COUNT(order_item_id) AS nb_items_bought\nFROM `thelook_prenom.silver_clean_orders_items`\nGROUP BY user_id;\n```"),
    md("### ✍️ À vous de jouer (Exercice 5 : Création du Mart Gold)\n**Consignes :**\nCréez une table `thelook_prenom.gold_daily_revenue` qui calcule :\n- Le chiffre d'affaires total (`SUM(sale_price)` nommé `total_revenue`)\n- Le nombre d'articles uniques vendus (`COUNT(order_item_id)` nommé `items_sold`)\nTout cela **par jour** (`order_date`). Triez le résultat du plus récent au plus ancien (`ORDER BY order_date DESC`)."),
    code("-- Écrivez votre requête d'agrégation Gold ici :\n\n", "sql")
]

cells_lab2 = [
    md("# 🧠 Lab 2 : SQL Avancé (UNNEST & Window Functions)\n\n**Objectifs :**\n- Gérer des données JSON/imbriquées (`STRUCT` et `ARRAY`)\n- Comprendre et utiliser `UNNEST`\n- Utiliser une Window Function (`ROW_NUMBER()`) pour un cas d'usage E-commerce"),
    md("*(Rappel : Tous vos travaux s'effectuent dans votre unique dataset `thelook_prenom`. Les couches sont représentées par les préfixes des tables : `bronze_`, `silver_`, `gold_`)*"),
    md("## Partie 1 : Les Tableaux et UNNEST()\nDans Google Cloud, les données Web (comme GA4 ou Firebase) sont souvent des tableaux d'objets (Arrays of Structs). Créons de fausses données imbriquées :"),
    code("/* ⚠️ Remplacez `thelook_prenom` */\nCREATE OR REPLACE TABLE `thelook_prenom.bronze_nested_orders` AS\nSELECT \n  'ORD999' as order_id, \n  'USER_1' as user_id,\n  [STRUCT('T-shirt' as product, 2 as quantity, 20.0 as price),\n   STRUCT('Jeans' as product, 1 as quantity, 50.0 as price)] as items\nUNION ALL\nSELECT 'ORD888', 'USER_2', [STRUCT('Sneakers' as product, 1 as quantity, 80.0 as price)];", "sql"),
    md("Si vous interrogez cette table `SELECT *`, la colonne `items` contient une liste. Pour analyser les ventes par produit, il faut **aplatir** cette liste avec `UNNEST()`.\n\n**Exemple de UNNEST :**\n```sql\nSELECT order_id, item.product, item.price\nFROM `thelook_prenom.bronze_nested_orders`,\nUNNEST(items) AS item;\n```"),
    md("### ✍️ À vous de jouer (Exercice 1)\n**Consignes :**\nÉcrivez une requête qui aplatit la table `bronze_nested_orders` et calcule le revenu total généré par CHAQUE produit (revenu = `quantity * price`).\nEnregistrez le résultat dans `thelook_prenom.gold_product_revenue`."),
    code("-- Écrivez votre requête d'aplatissement et agrégation ici :\n\n", "sql"),
    md("## Partie 2 : Les Window Functions\nLes fonctions de fenêtrage permettent de faire des calculs sur un ensemble de lignes (la fenêtre) liées à la ligne actuelle, sans réduire le nombre de lignes comme le ferait un `GROUP BY`.\n\n### 💡 Cas d'usage E-commerce : Trouver la dernière commande d'un client.\nImaginez qu'un client passe plusieurs commandes et que vous vouliez isoler uniquement sa **commande la plus récente**. \n\n**L'Exemple Parfait : `ROW_NUMBER()`**\n```sql\nWITH RankedOrders AS (\n  SELECT \n    order_id,\n    user_id,\n    order_date,\n    ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY order_date DESC) as rank_commande\n  FROM `thelook_prenom.silver_clean_orders_items`\n)\nSELECT *\nFROM RankedOrders\nWHERE rank_commande = 1; -- 1 = La plus récente pour chaque utilisateur !\n```"),
    md("### ✍️ À vous de jouer (Exercice 2)\n**Consignes :**\nEn utilisant les données de `thelook_prenom.silver_clean_orders_items` (créée au Lab 1), écrivez une requête avec une Window Function pour calculer le rang de chaque article par utilisateur, mais cette fois-ci **basé sur le montant le plus élevé** (`sale_price` du plus cher au moins cher). \n\nFiltrez ensuite pour n'afficher que l'article le plus cher jamais acheté par chaque client."),
    code("-- Écrivez votre requête avec Window Function ici :\n\n", "sql")
]

cells_lab3 = [
    md("# ⚙️ Lab 3 : Optimisation & Requêtes Planifiées\n\n**Objectifs :**\n- Réduire les coûts BigQuery avec le Partitionnement et le Clustering\n- Comparer les octets scannés (Full Scan vs Partition Scan)\n- Créer une Scheduled Query via le CLI"),
    md("*(Rappel : Toujours travailler dans le dataset `thelook_prenom`)*"),
    md("## Partie 1 : Partitionnement & Clustering\nPour éviter qu'une requête ne scanne toute la table (et coûte très cher), on découpe la table en \"partitions\" (généralement par date).\n\n**Exemple de création de table partitionnée :**\n```sql\nCREATE OR REPLACE TABLE `thelook_prenom.silver_partitioned_logs`\nPARTITION BY DATE(event_timestamp)\nCLUSTER BY user_id\nAS SELECT ...\n```"),
    md("### ✍️ À vous de jouer (Exercice 1)\n**Consignes :**\n1. Exécutez le code ci-dessous pour créer une table générant un million de logs avec une date aléatoire, partitionnée par `log_date` et clusterisée par `user_id`.\n2. Exécutez ensuite les deux requêtes `SELECT COUNT(*)` (une avec filtre de date, l'autre sans) et observez la différence de **Bytes processed** en haut à droite de la console BigQuery."),
    code("-- 1. Création de la table partitionnée et clustered\nCREATE OR REPLACE TABLE `thelook_prenom.silver_web_logs`\nPARTITION BY log_date\nCLUSTER BY user_id AS\nSELECT \n  DATE_ADD(CURRENT_DATE(), INTERVAL -CAST(FLOOR(RAND() * 30) AS INT64) DAY) AS log_date,\n  CONCAT('USER_', CAST(FLOOR(RAND() * 1000) AS STRING)) AS user_id,\n  'page_view' AS event_type\nFROM UNNEST(GENERATE_ARRAY(1, 1000000));\n", "sql"),
    code("-- 2. Comparez le coût (Regardez \"This query will process X MB\")\n\n-- Requête A (Sans filtre de date - Full Scan)\nSELECT COUNT(*) FROM `thelook_prenom.silver_web_logs` WHERE user_id = 'USER_50';\n\n-- Requête B (Avec filtre sur la partition - Partition Pruning)\nSELECT COUNT(*) FROM `thelook_prenom.silver_web_logs` WHERE log_date = CURRENT_DATE() AND user_id = 'USER_50';\n", "sql"),
    md("## Partie 2 : Requêtes Planifiées (Scheduled Queries)\nDans BigQuery, on peut automatiser une requête (ex: pour rafraîchir la couche Silver toutes les nuits). Sans DBT, c'est l'outil par défaut.\n\n**Exemple via le terminal (`bq`) :**\n```bash\nbq query \\\n  --use_legacy_sql=false \\\n  --display_name=\"Daily Refresh Silver (prenom)\" \\\n  --schedule=\"every 24 hours\" \\\n  'CREATE OR REPLACE TABLE `mon_projet.thelook_prenom.silver_ma_table` AS SELECT * FROM `mon_projet.thelook_prenom.bronze_ma_table`;'\n```"),
    md("### ✍️ À vous de jouer (Exercice 2)\n**Consignes :**\nDans un terminal (Cloud Shell ou votre VS Code), créez une requête planifiée qui va agréger les logs de `silver_web_logs` (nombre total d'événements par jour) et écrire le résultat dans `thelook_prenom.gold_daily_traffic` tous les jours à 02:00 du matin."),
    code("# Écrivez votre commande bash `bq query` ici :\n\n", "shellscript")
]

base_dir = "big_data/02_cours/day2_transformation/labs"
create_nb(cells_lab1, os.path.join(base_dir, "01_lab_medallion_bases.ipynb"))
create_nb(cells_lab2, os.path.join(base_dir, "02_lab_sql_avance.ipynb"))
create_nb(cells_lab3, os.path.join(base_dir, "03_lab_optimisation_automatisation.ipynb"))
print("All 3 labs updated with the single dataset rule!")
