

## 📋 Mission 2 : Constater le Moindre Privilège
Testons vos permissions réelles !
1. Dans le menu (☰), allez dans **IAM & Admin** > **IAM**.
2. Cherchez votre adresse e-mail.
3. Constatez vos rôles : `Viewer`, `BigQuery User`, etc.
4. **Essayez d'ajouter un rôle** : Cliquez sur "Accorder l'accès" (Grant Access). 
   - ➔ *Erreur ou bouton grisé : vous ne pouvez pas élever vos privilèges.*

---

## 📺 Mission 3 : Démo de l'Alerte Budgétaire et des Quotas
*Le formateur partage son écran pour montrer la sécurité financière.*
1. **Alerte Budgétaire (Billing)** : panneau **Billing** > **Budgets & alerts**, alerte fixée à **5 €** (e-mails d'alerte dès 10%, 50%, 90% et 100%).
2. **Plafonnement strict (Hard Quota)** : panneau **IAM & Admin** > **Quotas et limites système** (BigQuery) :
   - Quota journalier par utilisateur fixé à **33 Go / jour** (~100 Go sur 3 jours pour chaque étudiant, pour un total de ~600 Go garantissant de rester sous le 1 To mensuel gratuit).
   - Règle de bonne pratique par requête : garde-fou à **1 Go max par requête** (`maximum_bytes_billed`) pour éviter de griller son quota quotidien d'un coup.
   - En cas de dépassement, BigQuery **bloque la requête avant exécution** avec un coût de **0 €**.

---

## ✅ Checkpoint de validation
- [ ] L'étudiant a identifié son `Project ID` GCP.
- [ ] L'étudiant a compris pourquoi il ne peut pas modifier la sécurité (IAM).
- [ ] Le formateur a prouvé que la facturation du projet est sous contrôle.
