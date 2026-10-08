import json
import os

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [line + "\n" if i < len(text.split("\n"))-1 else line for i, line in enumerate(text.split("\n"))]}

def code(text, language="sql"):
    return {"cell_type": "code", "execution_count": None, "metadata": {"vscode": {"languageId": language}}, "outputs": [], "source": [line + "\n" if i < len(text.split("\n"))-1 else line for i, line in enumerate(text.split("\n"))]}

cells_lab1 = [
    md("# 🔄 Lab 1 : Fondations de l'Architecture Medallion\n\n**Objectifs :**\n- Créer ses propres datasets (rappel : nous partageons un projet GCP commun !)\n- Joindre des tables issues d'un dataset public (Bronze)\n- Nettoyer et filtrer des données brutes (Bronze ➔ Silver)\n- Comprendre Vues vs Tables Matérialisées\n- Agréger des données (Silver ➔ Gold)"),
    
    md("## ⚠️ Règle d'or : Projet Partagé\nNous travaillons tous sur le même projet Google Cloud. **Pour ne pas écraser le travail des autres, vous devez suffixer vos datasets par votre prénom ou trigramme.**\n\nExemple : `bronze_alice`, `silver_alice`, `gold_alice`."),
    
    md("### Étape 1 : Création de vos datasets"),
    
    code("export MY_NAME=\"prenom\" # Remplacer par votre prénom (sans espaces)\nexport PROJECT_ID=$(gcloud config get-value project)\n\nfor LAYER in bronze silver gold; do\n  bq mk --location=EU --dataset \"${PROJECT_ID}:${LAYER}_${MY_NAME}\"\ndone\n\necho \"Datasets créés pour $MY_NAME !\"", "shellscript"),
    
    md("### Étape 2 : Créer la table brute (Couche Bronze) avec TheLook eCommerce\nPour ce lab, nous allons travailler avec le dataset public e-commerce de Google : `bigquery-public-data.thelook_ecommerce`.\nAvant de transformer les données, nous voulons regrouper les informations des commandes (`orders`) et des articles commandés (`order_items`).\n\n**Exemple de requête sur un dataset public :**\n```sql\nSELECT order_id, status \nFROM `bigquery-public-data.thelook_ecommerce.orders` \nLIMIT 5;\n```"),
    
    md("### ✍️ À vous de jouer (Exercice 1 : Jointure Bronze)\n**Consignes :**\n1. Créez une table `bronze_prenom.raw_orders_items`.\n2. Faites une jointure (`JOIN`) entre `bigquery-public-data.thelook_ecommerce.orders` (alias `o`) et `bigquery-public-data.thelook_ecommerce.order_items` (alias `oi`) sur la clé `order_id`.\n3. Sélectionnez les colonnes suivantes : `o.order_id`, `o.user_id`, `o.created_at`, `o.status`, `oi.id AS order_item_id`, `oi.product_id`, `oi.sale_price`."),
    
    code("-- Écrivez votre création de table Bronze ici :\nCREATE OR REPLACE TABLE `bronze_prenom.raw_orders_items` AS\nSELECT \n  ...\n", "sql"),
    
    md("## Partie 1 : Transformation Bronze ➔ Silver\nDans la couche Silver, on nettoie, on type correctement les données et on filtre ce qui n'est pas pertinent.\n\n**Exemple de nettoyage (CAST, COALESCE) :**\n```sql\nSELECT \n  order_id,\n  DATE(created_at) AS date_propre,\n  COALESCE(sale_price, 0.0) AS prix_propre\nFROM `bronze_prenom.raw_orders_items`\nWHERE status IS NOT NULL;\n```"),
    
    md("### ✍️ À vous de jouer (Exercice 2 : Nettoyage Silver)\n**Consignes :** \n1. Créez une table `silver_prenom.clean_orders_items` à partir de votre table `bronze_prenom.raw_orders_items`.\n2. Convertissez le timestamp `created_at` en date simple (`DATE(created_at)`) et nommez la colonne `order_date`.\n3. Gardez uniquement les commandes dont le statut (`status`) est **'Complete'** ou **'Shipped'**.\n4. Assurez-vous d'exclure les articles dont le prix (`sale_price`) est nul ou négatif."),
    
    code("-- Écrivez votre requête de transformation Silver ici :\nCREATE OR REPLACE TABLE `silver_prenom.clean_orders_items` AS\nSELECT\n  ...\n", "sql"),
    
    md("## Partie 2 : Vue ou Table Matérialisée ?\nAu lieu d'une table physique qui doit être recalculée, on peut créer une vue matérialisée pour la couche Silver, ou une vue simple pour des requêtes de préparation.\n\n**Exemple de Vue Matérialisée :**\n```sql\nCREATE MATERIALIZED VIEW `silver_prenom.mv_shipped_orders` AS\nSELECT order_id, user_id FROM `bronze_prenom.raw_orders_items` WHERE status = 'Shipped';\n```"),
    
    md("### ✍️ À vous de jouer (Exercice 3 : Création d'une Vue)\n**Consignes :**\nCréez une vue classique (`CREATE OR REPLACE VIEW`) nommée `silver_prenom.v_high_value_items` qui ne sélectionne que les articles de `clean_orders_items` dont le `sale_price` est supérieur à 100$. Interrogez ensuite votre vue (via un `SELECT *`)."),
    
    code("-- Écrivez votre création de vue ici :\n\n", "sql"),
    
    md("## Partie 3 : Agrégation (Silver ➔ Gold)\nLa couche Gold contient les indicateurs métier, souvent hautement agrégés pour les tableaux de bord (BI).\n\n**Exemple d'agrégation :**\n```sql\nSELECT user_id, COUNT(order_item_id) AS nb_items_bought\nFROM `silver_prenom.clean_orders_items`\nGROUP BY user_id;\n```"),
    
    md("### ✍️ À vous de jouer (Exercice 4 : Création du Mart Gold)\n**Consignes :**\nCréez une table `gold_prenom.daily_revenue` qui calcule :\n- Le chiffre d'affaires total (`SUM(sale_price)` nommé `total_revenue`)\n- Le nombre d'articles uniques vendus (`COUNT(order_item_id)` nommé `items_sold`)\nTout cela **par jour** (`order_date`). Triez le résultat du plus récent au plus ancien (`ORDER BY order_date DESC`)."),
    
    code("-- Écrivez votre requête d'agrégation Gold ici :\n\n", "sql")
]

nb = {
    "cells": cells_lab1,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"codemirror_mode": {"name": "ipython", "version": 3}, "file_extension": ".py", "mimetype": "text/x-python", "name": "python", "nbconvert_exporter": "python", "pygments_lexer": "ipython3", "version": "3.10.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

file_path = "big_data/02_cours/day2_transformation/labs/01_lab_medallion_bases.ipynb"
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write("\n")

print("Lab 1 patched with TheLook eCommerce join!")
