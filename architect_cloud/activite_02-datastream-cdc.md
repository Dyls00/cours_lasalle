# 🔄 Activité Pratique : Déploiement d'un Pipeline CDC avec Datastream

> **Module :** Architecture Data Cloud sur Google Cloud Platform 
> **Niveau :** Master 2 Informatique / Cloud & Data Architecture  
> **Format :** Individuel | **Durée estimée :** 1h

---

## 🎯 Objectifs

* Découvrir le pattern fondamental du **Change Data Capture (CDC)** sur Google Cloud.
* Connecter une base opérationnelle **PostgreSQL (Cloud SQL)** à un entrepôt de données **BigQuery** sans impacter les performances de production.
* Configurer et superviser un flux temps réel serverless avec **Google Cloud Datastream**.
* Valider la réplication continue en observant la propagation immédiate des transactions dans BigQuery.

---

## 📋 Étape 1 : Vérification des Prérequis Source (PostgreSQL)

Pour que Datastream puisse capturer les modifications depuis le journal de transactions (**WAL**), l'instance Cloud SQL doit autoriser le décodage logique.

| Paramètre | Valeur attendue |
|---|---|
| **Instance source** | `fastmarket-VOTRE_NOM` (créée à l'activité précédente) |
| **Drapeau de base de données (*Flag*)** | `cloudsql.logical_decoding = on` |
| **Base de données source** | `fastmarket_shop` |
| **Compte de connexion** | `postgres_user` (ou utilisateur disposant du rôle `REPLICATION`) |

> 💡 **Vérification rapide :**  
> Dans la console Cloud SQL, vérifiez dans l'onglet **Configuration** que le drapeau `cloudsql.logical_decoding` est bien activé. Si vous devez l'ajouter, un redémarrage de l'instance sera requis.

---

## 🔌 Étape 2 : Création des Profils de Connexion

Depuis la console GCP, rendez-vous dans le service **Datastream > Profils de connexion** (*Connection Profiles*) et créez les deux extrémités du pipeline :

### 1. Profil Source (PostgreSQL)
* **Nom du profil :** `src-postgres-fastmarket`
* **Type :** PostgreSQL
* **Hôte & Port :** IP de votre instance Cloud SQL / Port `5432`
* **Base de données & Identifiants :** `fastmarket_shop` / utilisateur et mot de passe de votre base
* **Méthode de connectivité :** Liste d'adresses IP autorisées (*IP allowlisting*) ou Connectivité privée

> ⚠️ **Indice Réseau :**  
> Si vous utilisez la méthode par IP autorisée, Datastream affiche une liste d'adresses IP publiques Google. Pensez à ajouter ces IPs dans la section **Réseaux autorisés** (*Authorized Networks*) de votre instance Cloud SQL !

### 2. Profil Destination (BigQuery)
* **Nom du profil :** `dst-bigquery-analytics`
* **Type :** BigQuery
* **Région :** Belgique (`europe-west1`)

---

## 🌊 Étape 3 : Création et Démarrage du Flux (Stream)

Dans **Datastream > Flux** (*Streams*), créez un nouveau flux de réplication en renseignant les informations suivantes :

| Paramètre | Valeur attendue |
|---|---|
| **Nom du flux** | `stream-fastmarket-cdc` |
| **Profil source** | `src-postgres-fastmarket` |
| **Profil de destination** | `dst-bigquery-analytics` |
| **Objets sources à répliquer** | Schéma `public` (sélectionnez toutes les tables : `users`, `products`, `orders`, etc.) |
| **Type de réplication** | Rétroaction historique + Modifications continues (*Backfill + CDC*) |
| **Nom du jeu de données BigQuery cible** | Déduit du nom de la source ou personnalisé (ex: `fastmarket_shop_cdc`) |

> 🔍 **Avant de démarrer le flux :**  
> Cliquez sur **Valider le flux** (*Run validation*). Datastream vérifie automatiquement la connectivité, la présence des slots de réplication et les droits d'accès. Corrigez les éventuelles alertes avant de lancer le flux.

---

## ✅ Étape 4 : Validation du Streaming Temps Réel

Une fois le flux au statut **En cours d'exécution** (*Running*) :

1. **Vérification de l'historique initial dans BigQuery :**
   * Rendez-vous dans **BigQuery Studio**.
   * Localisez le jeu de données créé par Datastream et vérifiez que les tables sont bien répliquées.

2. **Test de capture d'une transaction en direct :**
   * Connectez-vous à votre base PostgreSQL (via Cloud Shell ou client SQL).
   * Insérez un nouvel utilisateur ou une commande de test :
     ```sql
     INSERT INTO users (email, password_hash, first_name, last_name, country)
     VALUES ('test.cdc@datakoko.com', 'hash123', 'Thomas', 'Pesquet', 'France');
     ```
   * Dans BigQuery, interrogez la table `users` correspondante :
     ```sql
     SELECT * FROM `fastmarket_shop_cdc.users` 
     WHERE email = 'test.cdc@datakoko.com';
     ```
   * **Constatez :** La ligne apparaît dans BigQuery en moins de 5 secondes, sans jamais avoir exécuté d'export ou de script batch !
