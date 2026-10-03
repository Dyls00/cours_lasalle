# Module 3.4 — Visualisation avec Looker Studio

## 🎯 Objectifs
Connecter Looker Studio directement à notre table **Gold BigQuery** (`fct_daily_sales`) et créer un tableau de bord analytique d'une page.

---

## 📋 Étapes de Création du Tableau de Bord

1. **Connexion aux Données** :
   - Ouvrez [Looker Studio](https://lookerstudio.google.com/).
   - Cliquez sur **Créer** > **Rapport**.
   - Sélectionnez le connecteur **BigQuery**.
   - Choisissez votre **Projet GCP** > Dataset **`gold`** > Table **`fct_daily_sales`**.

2. **Ajout des Indicateurs Clés (KPI Scorecards)** :
   - Nombre total d'utilisateurs actifs (`SUM(active_users)`).
   - Nombre de vues de pages (`SUM(total_page_views)`).
   - Nombre de commandes payées (`SUM(total_purchases)`).

3. **Graphiques & Filtres** :
   - **Graphique en courbes (Time Series)** : Évolution des utilisateurs actifs par `event_date`.
   - **Graphique en barres** : Répartition des ventes par `device_os`.
   - **Filtre dynamique** : Liste déroulante sur la période et le système d'exploitation (`device_os`).
