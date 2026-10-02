# 📚 Parcours d'Apprentissage dlt (dlt-hub Fundamentals)

Ce dossier regroupe les notebooks officiels de formation créés par l'équipe de **dltHub** (*dlt Fundamentals Course*), adaptés pour le cours de Big Data.

Chaque notebook est conçu pour être exécuté pas à pas :
- **En local** dans VSCode
- **Dans Google Colab** directement en un clic grâce au badge [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com) situé en tête de chaque fichier.

---

## 🎯 Programme Principal Jour 1 (Module 1.5 - Ingestion)

Pour ce premier jour, nous nous concentrons sur les **2 notebooks fondamentaux** permettant de maîtriser les concepts clés sans surcharge cognitive :

| # | Notebook | Concepts Clés | Durée Estimée |
|---|---|---|---|
| **01** | [06_ingestion_intro_dlt.ipynb](labs/06_ingestion_intro_dlt.ipynb) | Découverte de `dlt`, premier pipeline sur données semi-structurées, chargement dans DuckDB, exploration via `sql_client` et datasets. | 25 min |
| **02** | [07_ingestion_dlt_sources_and_resources.ipynb](labs/07_ingestion_dlt_sources_and_resources.ipynb) | Les briques fondamentales : `@dlt.resource` et `@dlt.source`, gestion des flux/générateurs Python (`yield`), transformers et première ingestion d'API REST. | 35 min |

---

## 🎁 Dossier Bonus : Pour Aller Plus Loin

Pour les étudiants qui avancent plus vite ou souhaitent approfondir les mécaniques avancées de production, 3 notebooks complémentaires sont disponibles dans le sous-dossier [`bonus/`](bonus/) :

| # | Notebook Bonus | Concepts Clés |
|---|---|---|
| **03** | [03_lesson_pagination_and_configuration.ipynb](bonus/03_lesson_pagination_and_configuration.ipynb) | Pagination automatique des APIs, client HTTP `RESTClient`, et gestion sécurisée des secrets (`secrets.toml`). |
| **04** | [04_lesson_write_disposition_and_incremental.ipynb](bonus/04_lesson_write_disposition_and_incremental.ipynb) | Modes d'écriture (`append`, `replace`, `merge` avec déduplication) et **chargement incrémental** via curseurs temporels. |
| **05** | [05_lesson_inspecting_and_adjusting_schema.ipynb](bonus/05_lesson_inspecting_and_adjusting_schema.ipynb) | Inférence automatique de schéma, normalisation des structures JSON imbriquées, et contrats de données (*Schema Contracts*). |

---

## 🚀 Comment lancer les notebooks ?

### Option A : En local avec VSCode (Environnement virtuel)
1. Ouvrez le dossier du projet dans VSCode.

### Option B : Dans Google Colab (Zéro installation)
1. Ouvrez le notebook et cliquez sur le badge **Open in Colab** en haut de la page.
2. Exécutez la première cellule `!pip install "dlt[duckdb]"` pour installer l'environnement Colab.