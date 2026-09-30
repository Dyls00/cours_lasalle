-- ============================================================================
-- MODULE 1.1 : LE PARADIGME BIG DATA & COMPARAISON OLTP vs OLAP
-- ============================================================================
-- Objectif : Illustrer le fonctionnement d'une base analytique en colonnes (BigQuery)
-- comparativement à une base transactionnelle orientée lignes (PostgreSQL/MySQL).
-- ============================================================================
-- ----------------------------------------------------------------------------
-- 1. Requête analytique sur BigQuery (Dataset public wikipedia ou github)
-- BigQuery stocke les données par COLONNE (Capacitor/Colossus).
-- Lors de l'exécution ci-dessous, seules 2 colonnes (title, views) sont lues !
-- ----------------------------------------------------------------------------
SELECT title,
    SUM(views) AS total_views
FROM `bigquery-public-data.wikipedia.wiki1k`
WHERE date >= '2023-01-01'
GROUP BY 1
ORDER BY total_views DESC
LIMIT 10;
-- 💡 QUESTION POUR LES ÉTUDIANTS :
-- Pourquoi cette requête scanne-t-elle seulement quelques Mo/Go alors que 
-- sur BigQuery alors que la table contient plusieurs téraoctets ?
-- Reponse : Stockage en colonnes + lecture sélective uniquement des colonnes invoquées.