# Module 1.2 — GCP, Coûts, Gouvernance et Configuration des Alertes

## 🎯 Objectifs
- Comprendre la structure de gouvernance GCP (Organisation > Dossier > Projet > Ressources).
- Configurer les rôles IAM minimaux (Principle of Least Privilege).
- Choisir la bonne région de stockage (EU / `europe-west9` Paris pour conformité RGPD).
- Configurer une alerte budgétaire en direct pour éviter les surcoûts.

---

## 1. Structure IAM recommandée
Pour les exercices Data Engineering :
- **Data Engineer** : `roles/bigquery.admin`, `roles/storage.admin`
- **Lecteur / Analyste** : `roles/bigquery.dataViewer`, `roles/bigquery.jobUser`

---

## 2. Configuration d'une Alerte Budgétaire (Budget Alert)

1. Rendez-vous dans la **Google Cloud Console** > **Billing** (Facturation) > **Budgets & alerts**.
2. Cliquez sur **Create Budget**.
3. **Montant du budget** : Définir un plafond mensuel (ex: **10 €** ou **20 €** pour les TPs).
4. **Seuils d'alerte** :
   - 50% du budget (5 €) -> Alerte e-mail
   - 80% du budget (8 €) -> Alerte e-mail
   - 100% du budget (10 €) -> Alerte e-mail
5. Enregistrer le budget.

---

## 3. Emplacement des Données (Data Residency)
> ⚠️ **Règle fondamentale** : Toujours créer ses datasets BigQuery et buckets Cloud Storage dans la même région (ex: `EU` multi-region ou `europe-west9` Paris).
> Une jointure ou un chargement entre deux régions différentes échouera sur BigQuery !
