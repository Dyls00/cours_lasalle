### Programme Intro Big Data 3 jours (21h)

Environ 4h30 de théorie (~20 %) pour 16h30 de pratique.
Ceci inclus une évaluation pratique.

#### Jour 1 : Comprendre, stocker, ingérer

| Module                            | Durée | Type                        | Contenu                                                                                                                                                                  |
| --------------------------------- | ----- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1.1 Le paradigme Big Data**     | 1h15  | Théorie + démo              | 4V ; OLTP vs OLAP ; calcul distribué ; découplage stockage/calcul ; Lake / DWH / Lakehouse. Démo : requête sur une grosse table publique BigQuery |
| **1.2 GCP, coûts, gouvernance**   | 0h45  | Mixte                       | Projets, IAM, localisation EU (RGPD, résidence des données), modèle de coûts, alertes de budget configurées en direct                                                    |
| **1.3 Prise en main**             | 0h30  | Pratique                    | UI BigQuery: requêtes sur un dataset public, dry run                                                                                  |
| **1.4 Lake vs Data Warehouse**    | 1h15  | Pratique                    | Cloud Shell Editor (ou VS Code local + gcloud),création & ingestion dans bucket, JSON/logs, table externe, chargement en table native, comparaison des bytes scannés                                                                              |
| **1.5 ELT et ingestion avec dlt** | 3h15  | Théorie (30 min) + pratique | API REST → BigQuery (Bronze), schema evolution, chargement incrémental                                                                                                   |

#### Jour 2 : Analyser et transformer

| Module                                   | Durée | Type                        | Contenu                                                                                     |
| ---------------------------------------- | ----- | --------------------------- | ------------------------------------------------------------------------------------------- |
| **2.1 Performance et coûts**             | 1h00  | Mixte                       | Partitionnement, clustering, cache, exercice avant/après sur la grosse table publique       |
| **2.2 SQL analytique et semi-structuré** | 2h00  | Pratique                    | CTE, UNNEST/STRUCT/ARRAY, window functions sur les JSON du fil rouge                        |
| **2.3 Modélisation et Medallion**        | 0h30  | Théorie                     | Modélisation d'une BDD analytique.<br>(Étoile vs dénormalisation, Bronze/Silver/Gold)       |
| **2.4 Transformation avec dbt**          | 3h30  | Théorie (30 min) + pratique | Projet dbt, couche Silver (nettoyage, typage, déduplication), couche Gold (agrégats métier) |

#### Jour 3 : Fiabiliser, streamer, évaluer

| Module                                     | Durée | Type                        | Contenu                                                                                                                                                                                                                                                        |
| ------------------------------------------ | ----- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **3.1 Qualité des données**                | 1h00  | Mixte                       | Data contracts, dbt test, fraîcheur des données, <br>- exercice « casser un test »                                                                                                                                                                             |
| **3.2 Orchestration**                      | 0h45  | Pratique                    | Script bash ou Github Actions si possible  : dlt → dbt run → dbt test                                                                                                                                                                                          |
| **3.3 Vélocité : Pub/Sub, Beam, Dataflow** | 2h15  | Théorie (30 min) + pratique | Batch vs streaming, fenêtrage, gestion des merges et des queues. Rejeu du jeu de données du fil rouge, pipeline Beam en local, puis déploiement sur Dataflow vers BigQuery                                                                                     |
| **3.4 Looker Studio**                      | 0h30  | Pratique                    | Dashboard d'une page sur la table Gold                                                                                                                                                                                                                         |
| **3.5 Cas pratique évalué**                | 2h30  | Examen en Autonomie         | Mission sur un dépôt Git fourni : Ingestion d'une API spécifique, aplatissement du JSON dans BigQuery, création d'un modèle dbt documenté et testé, et génération d'une requête SQL d'analyse descriptive métier finale.<br><br>+ quelques qestions théoriques |

