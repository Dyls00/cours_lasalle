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
    md("# 🔄 Lab 1 : Fondations de l'Architecture Medallion\n\n**Objectifs :**\n- Créer ses propres datasets (rappel : nous partageons un projet GCP commun !)\n- Nettoyer des données brutes (Bronze ➔ Silver)\n- Comprendre Vues vs Tables Matérialisées\n- Agréger des données (Silver ➔ Gold)"),
    md("## ⚠️ Règle d'or : Projet Partagé\nNous travaillons tous sur le même projet Google Cloud. **Pour ne pas écraser le travail des autres, vous devez suffixer vos datasets par votre prénom ou trigramme.**\n\nExemple : `bronze_alice`, `silver_alice`, `gold_alice`."),
    md("### Étape 1 : Création de vos datasets"),
    code("export MY_NAME=\"prenom\" # Remplacer par votre prénom (sans espaces)\nexport PROJECT_ID=$(gcloud config get-value project)\n\nfor LAYER in bronze silver gold; do\n  bq mk --location=EU --dataset \"${PROJECT_ID}:${LAYER}_${MY_NAME}\"\ndone\n\necho \"Datasets créés pour $MY_NAME !\"", "shellscript"),
    md("### Étape 2 : Créer des données brutes (Bronze)\nExécutez ce code SQL pour simuler des données de ventes contenant des erreurs (doublons, nulls)."),
    code("/* À EXÉCUTER DANS LA CONSOLE BIGQUERY */\n/* ⚠️ Remplacez `bronze_prenom` par votre dataset */\nCREATE OR REPLACE TABLE `bronze_prenom.raw_orders` AS\nSELECT 'ORD001' as id, '2023-10-01' as order_date, '150.50' as amount, 'USER_1' as user_id UNION ALL\nSELECT 'ORD002', '2023-10-01', 'NULL', 'USER_2' UNION ALL\nSELECT 'ORD001', '2023-10-01', '150.50', 'USER_1' UNION ALL -- Doublon !\nSELECT 'ORD003', '2023-10-02', '-50.00', 'USER_3'; -- Montant négatif invalide", "sql"),
    md("## Partie 1 : Transformation Bronze ➔ Silver\n\n**Exemple de nettoyage :**\nVoici comment caster une colonne et remplacer les valeurs nulles en SQL :\n```sql\nSELECT \n  id,\n  CAST(order_date AS DATE) AS date_propre,\n  COALESCE(SAFE_CAST(amount AS FLOAT64), 0.0) AS montant_propre\nFROM `bronze_prenom.ma_table`\nWHERE amount IS NOT NULL;\n```"),
    md("### ✍️ À vous de jouer (Exercice 1)\n**Consignes :** \n1. Créez une table `silver_prenom.clean_orders` à partir de `bronze_prenom.raw_orders`.\n2. Convertissez la date en `DATE` et le montant en `FLOAT64`.\n3. Supprimez les doublons (utilisez `DISTINCT` ou `GROUP BY`).\n4. Filtrez les commandes où le montant est négatif ou string 'NULL'."),
    code("-- Écrivez votre requête de transformation ici :\nCREATE OR REPLACE TABLE `silver_prenom.clean_orders` AS\nSELECT\n  ...\n", "sql"),
    md("## Partie 2 : Vue ou Table Matérialisée ?\nAu lieu d'une table physique qui doit être recalculée, on peut créer une vue matérialisée.\n\n**Exemple :**\n```sql\nCREATE MATERIALIZED VIEW `silver_prenom.mv_clean_orders` AS\nSELECT id, user_id FROM `bronze_prenom.raw_orders`;\n```"),
    md("### ✍️ À vous de jouer (Exercice 2)\n**Consignes :**\nCréez une vue `silver_prenom.v_orders` (vue classique, `CREATE VIEW`) et interrogez-la. Notez que la vue classique recalcule tout à chaque fois, contrairement à la table ou à la vue matérialisée."),
    code("-- Écrivez votre création de vue ici :\n\n", "sql"),
    md("## Partie 3 : Agrégation (Silver ➔ Gold)\nLa couche Gold contient les indicateurs métier.\n\n**Exemple d'agrégation :**\n```sql\nSELECT user_id, COUNT(id) AS nb_orders\nFROM `silver_prenom.clean_orders`\nGROUP BY user_id;\n```"),
    md("### ✍️ À vous de jouer (Exercice 3)\n**Consignes :**\nCréez une table `gold_prenom.daily_revenue` qui calcule le chiffre d'affaires total (`SUM`) et le nombre de commandes par jour (`order_date`)."),
    code("-- Écrivez votre requête d'agrégation Gold ici :\n\n", "sql")
]

cells_lab2 = [
    md("# 🧠 Lab 2 : SQL Avancé (UNNEST & Window Functions)\n\n**Objectifs :**\n- Gérer des données JSON/imbriquées (`STRUCT` et `ARRAY`)\n- Comprendre et utiliser `UNNEST`\n- Utiliser une Window Function (`ROW_NUMBER()`) pour un cas d'usage E-commerce"),
    md("*(N'oubliez pas d'utiliser VOS datasets avec votre prénom : `bronze_prenom`, `silver_prenom`, etc.)*"),
    md("## Partie 1 : Les Tableaux et UNNEST()\nDans Google Cloud, les données Web (comme GA4 ou Firebase) sont souvent des tableaux d'objets (Arrays of Structs). Créons de fausses données imbriquées :"),
    code("/* ⚠️ Remplacez `bronze_prenom` */\nCREATE OR REPLACE TABLE `bronze_prenom.nested_orders` AS\nSELECT \n  'ORD999' as order_id, \n  'USER_1' as user_id,\n  [STRUCT('T-shirt' as product, 2 as quantity, 20.0 as price),\n   STRUCT('Jeans' as product, 1 as quantity, 50.0 as price)] as items\nUNION ALL\nSELECT 'ORD888', 'USER_2', [STRUCT('Sneakers' as product, 1 as quantity, 80.0 as price)];", "sql"),
    md("Si vous interrogez cette table `SELECT *`, la colonne `items` contient une liste. Pour analyser les ventes par produit, il faut **aplatir** cette liste avec `UNNEST()`.\n\n**Exemple de UNNEST :**\n```sql\nSELECT order_id, item.product, item.price\nFROM `bronze_prenom.nested_orders`,\nUNNEST(items) AS item;\n```"),
    md("### ✍️ À vous de jouer (Exercice 1)\n**Consignes :**\nÉcrivez une requête qui aplatit la table `nested_orders` et calcule le revenu total généré par CHAQUE produit (revenu = `quantity * price`).\nEnregistrez le résultat dans `gold_prenom.product_revenue`."),
    code("-- Écrivez votre requête d'aplatissement et agrégation ici :\n\n", "sql"),
    md("## Partie 2 : Les Window Functions\nLes fonctions de fenêtrage permettent de faire des calculs sur un ensemble de lignes (la fenêtre) liées à la ligne actuelle, sans réduire le nombre de lignes comme le ferait un `GROUP BY`.\n\n### 💡 Cas d'usage E-commerce : Trouver la dernière commande d'un client.\nImaginez qu'un client passe plusieurs commandes et que vous vouliez isoler uniquement sa **commande la plus récente**. \n\n**L'Exemple Parfait : `ROW_NUMBER()`**\n```sql\nWITH RankedOrders AS (\n  SELECT \n    id,\n    user_id,\n    order_date,\n    ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY order_date DESC) as rank_commande\n  FROM `silver_prenom.clean_orders`\n)\nSELECT *\nFROM RankedOrders\nWHERE rank_commande = 1; -- 1 = La plus récente pour chaque utilisateur !\n```"),
    md("### ✍️ À vous de jouer (Exercice 2)\n**Consignes :**\nEn utilisant les données de `silver_prenom.clean_orders` (créée au Lab 1), écrivez une requête avec une Window Function pour calculer le rang de chaque commande par utilisateur, mais cette fois-ci **basé sur le montant le plus élevé** (du plus cher au moins cher). \n\nFiltrez ensuite pour n'afficher que la commande la plus chère de chaque client."),
    code("-- Écrivez votre requête avec Window Function ici :\n\n", "sql")
]

cells_lab3 = [
    md("# ⚙️ Lab 3 : Optimisation & Requêtes Planifiées\n\n**Objectifs :**\n- Réduire les coûts BigQuery avec le Partitionnement et le Clustering\n- Comparer les octets scannés (Full Scan vs Partition Scan)\n- Créer une Scheduled Query via le CLI"),
    md("*(Rappel : Remplacez toujours `prenom` par votre prénom)*"),
    md("## Partie 1 : Partitionnement & Clustering\nPour éviter qu'une requête ne scanne toute la base de données (et coûte très cher), on découpe la table en \"partitions\" (généralement par date).\n\n**Exemple de création de table partitionnée :**\n```sql\nCREATE OR REPLACE TABLE `silver_prenom.partitioned_logs`\nPARTITION BY DATE(event_timestamp)\nCLUSTER BY user_id\nAS SELECT ...\n```"),
    md("### ✍️ À vous de jouer (Exercice 1)\n**Consignes :**\n1. Exécutez le code ci-dessous pour créer une table générant un million de logs avec une date aléatoire, partitionnée par `log_date` et clusterisée par `user_id`.\n2. Exécutez ensuite les deux requêtes `SELECT COUNT(*)` (une avec filtre de date, l'autre sans) et observez la différence de **Bytes processed** en haut à droite de la console BigQuery."),
    code("-- 1. Création de la table partitionnée et clustered\nCREATE OR REPLACE TABLE `silver_prenom.web_logs`\nPARTITION BY log_date\nCLUSTER BY user_id AS\nSELECT \n  DATE_ADD(CURRENT_DATE(), INTERVAL -CAST(FLOOR(RAND() * 30) AS INT64) DAY) AS log_date,\n  CONCAT('USER_', CAST(FLOOR(RAND() * 1000) AS STRING)) AS user_id,\n  'page_view' AS event_type\nFROM UNNEST(GENERATE_ARRAY(1, 1000000));\n", "sql"),
    code("-- 2. Comparez le coût (Regardez \"This query will process X MB\")\n\n-- Requête A (Sans filtre de date - Full Scan)\nSELECT COUNT(*) FROM `silver_prenom.web_logs` WHERE user_id = 'USER_50';\n\n-- Requête B (Avec filtre sur la partition - Partition Pruning)\nSELECT COUNT(*) FROM `silver_prenom.web_logs` WHERE log_date = CURRENT_DATE() AND user_id = 'USER_50';\n", "sql"),
    md("## Partie 2 : Requêtes Planifiées (Scheduled Queries)\nDans BigQuery, on peut automatiser une requête (ex: pour rafraîchir la couche Silver toutes les nuits). Sans DBT, c'est l'outil par défaut.\n\n**Exemple via le terminal (`bq`) :**\n```bash\nbq query \\\n  --use_legacy_sql=false \\\n  --display_name=\"Daily Refresh Silver (prenom)\" \\\n  --schedule=\"every 24 hours\" \\\n  'CREATE OR REPLACE TABLE `mon_projet.silver_prenom.ma_table` AS SELECT * FROM `mon_projet.bronze_prenom.ma_table`;'\n```"),
    md("### ✍️ À vous de jouer (Exercice 2)\n**Consignes :**\nDans un terminal (Cloud Shell ou votre VS Code), créez une requête planifiée qui va agréger les logs de `web_logs` (nombre total d'événements par jour) et écrire le résultat dans `gold_prenom.daily_traffic` tous les jours à 02:00 du matin."),
    code("# Écrivez votre commande bash `bq query` ici :\n\n", "shellscript")
]

base_dir = "big_data/02_cours/day2_transformation/labs"
create_nb(cells_lab1, os.path.join(base_dir, "01_lab_medallion_bases.ipynb"))
create_nb(cells_lab2, os.path.join(base_dir, "02_lab_sql_avance.ipynb"))
create_nb(cells_lab3, os.path.join(base_dir, "03_lab_optimisation_automatisation.ipynb"))
