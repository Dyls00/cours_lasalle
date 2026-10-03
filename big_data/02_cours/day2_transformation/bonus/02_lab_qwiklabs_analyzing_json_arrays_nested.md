# 🧪 TP Google Lab : Analyzing JSON, Array, and Nested Data in BigQuery

---

## 🎯 Objectifs du Lab
1. Comprendre la manipulation des types complexes `ARRAY` (Listes) et `STRUCT` (Enregistrements imbriqués).
2. Utiliser la fonction SQL `UNNEST()` pour aplatir des collections de données imbriquées.
3. Inpacter un fichier JSONL contenant des structures complexes (`RECORD` / `REPEATED`).
4. Extraire des métriques d'analyse sans altérer la hiérarchie originale.

---

## 📋 Tâche 1 : Expérimentation des Littéraux `ARRAY` et `STRUCT`

Exécutez cette première requête dans l'interface BigQuery :

```sql
-- 1. Création d'un ARRAY (Liste d'éléments du même type)
SELECT ['Apple', 'Banana', 'Orange', 'Mango'] AS fruits_array;

-- 2. Création d'un STRUCT (Objet composé de paires clé-valeur)
SELECT STRUCT("Pierre" AS runner_name, [23.4, 26.1, 25.8] AS lap_times) AS runner;
```

---

## 📋 Tâche 2 : Ingestion de Données Semi-Structurées (Résultats de Course)

1. Créez un dataset nommé `racing` :
```bash
export PROJECT_ID=$(gcloud config get-value project)
bq mk --location=EU --dataset "${PROJECT_ID}:racing"
```

2. Chargez les données du fichier public `race_results.json` :
```bash
bq load \
    --source_format=NEWLINE_DELIMITED_JSON \
    --autodetect \
    "${PROJECT_ID}:racing.race_results" \
    gs://spls/gsp416/race_results.json
```

3. Observez le schéma généré :
   - La colonne `participants` est de type `RECORD` (STRUCT) avec le mode `REPEATED` (ARRAY).

---

## 📋 Tâche 3 : Aplatir les Arrays avec `UNNEST()`

Si vous essayez d'accéder directement à `participants.name`, BigQuery renverra une erreur car `participants` est un tableau de plusieurs éléments par ligne !

Il faut utiliser la jointure avec `UNNEST()` :

```sql
SELECT
  r.race_name,
  r.round,
  p.name AS participant_name,
  p.position
FROM
  `racing.race_results` AS r,
  UNNEST(r.participants) AS p
ORDER BY
  r.round, p.position;
```

---

## 📋 Tâche 4 : Calcul d'Agrégats sur Structures Imbriquées

Compter le nombre total de participants par course :

```sql
SELECT
  r.race_name,
  COUNT(p.name) AS total_participants,
  AVG(p.position) AS avg_position
FROM
  `racing.race_results` AS r,
  UNNEST(r.participants) AS p
GROUP BY
  r.race_name
ORDER BY
  total_participants DESC;
```

---

## ✅ Checkpoint d'évaluation (Style Qwiklabs)
- [ ] Dataset `racing` créé.
- [ ] Table `race_results` chargée avec succès depuis le JSON Cloud Storage.
- [ ] Maîtrise de la syntaxe `UNNEST(array_field) AS alias` pour l'aplatissement.
