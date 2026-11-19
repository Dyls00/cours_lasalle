---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #f8fafc
color: #0f172a
header: "Architecture Data Cloud — M2 Informatique"
footer: "Du Monolithe à l'Architecture data moderne | FastMarket Case"
style: |
  section {
    font-size: 24px;
    font-family: 'Inter', system-ui, sans-serif;
  }
  h1 { color: #0f172a; border-bottom: 3px solid #db2777; padding-bottom: 8px; }
  h2 { color: #1e3a8a; }
  h3 { color: #be185d; }
  code { background: #e2e8f0; color: #0f172a; border-radius: 4px; padding: 2px 6px; }
  pre { background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 12px; }
  pre code { background: transparent; color: #f8fafc; padding: 0; }
  strong { color: #1e3a8a; }
  em { color: #be185d; font-style: normal; font-weight: 600; }
  blockquote { background: #fce7f3; border-left: 8px solid #db2777; color: #0f172a; padding: 10px 16px; }
---

<!-- _class: lead -->

# ☁️ Architecture Data Cloud sur GCP
## Du Monolithe à l'Architecture data moderne

### Thèmes de la journée
- **Défis de l'OLTP combinés aux requêtes analytique** : Conflits de verrous & MVCC sur PostgreSQL
- **Découplage microservices** : Du monolithe à l'architecture distribuée

---

## 🎯 Contexte & Objectifs Pédagogiques

>  **Notre mission de la semaine** : Sortir d'une vision monolithique centralisée pour concevoir une architecture data cloud résiliente et conforme aux standards industriels sur **Google Cloud Platform**.

### Objectifs d'apprentissage du Jour 1
1. **Comprendre la fracture OLTP vs OLAP** : Pourquoi mutualiser transactions et analytics détruit la production.
2. **Diagnostiquer les pannes réelles** : Observer l'utilisation des ressources, l'invalidation de cache et le *Table Bloat*.
3. **Maîtriser les compromis des microservices** : Comprendre les bénéfices et limites de l'architecture en microservices.
4. **Implémenter le streaming d'événements** : Remplacer la "double insertion"par le *CDC* basé sur le journal WAL.

---

## 🛍️ Le Cas Fil Rouge : "FastMarket"

### L'Entreprise & l'Infrastructure
- **FastMarket** : Plateforme e-commerce en hyper-croissance
  - **500 000** utilisateurs actifs
  - **25 000** commandes / jour (pics à **x15** au Black Friday)
- **Infrastructure actuelle** :
  - Monolithe applicatif connecté à une **base unique PostgreSQL mutualisée** (métier + reporting).

> ⚠️ **Alerte Direction Technique** : Lors du dernier Black Friday, le panier est resté bloqué **42 minutes**, générant une perte sèche estimée à **180 000 €**.

---

## 🏛️ Anatomie du Monolithe FastMarket

```
   [ Client Web / Mobile ]
              │ (HTTP REST)
              ▼
   ┌─────────────────────────────────────────────────────────────┐
   │                  MONOLITHE APPLICATIF                       │
   │   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
   │   │    Payment    │  │ Shopping Cart │  │   Inventory   │   │
   │   └───────┬───────┘  └───────┬───────┘  └───────┬───────┘   │
   └───────────┼──────────────────┼──────────────────┼───────────┘
               │                  │                  │
               └─────────► ┌──────┴──────┐ ◄─────────┘
                           │  PostgreSQL │ (Instance Unique OLTP)
                           │  Mutualisée │ ◄── Requêtes Analytics BI
                           └─────────────┘
```

>  **Problème architectural fondamental** : Tous les modules applicatifs et les outils BI tapent sur le *même moteur de stockage* et le *même pool de connexions*.

---

##  Les Symptômes Métiers de la Crise

| Métier / Pôle | Constat & Impact |
|---|---|
| **Marketing & BI** | *"Le site freeze le matin"*<br/>Rapports lancés à 9h00 → l'API web s'effondre et bloque les paniers. |
| **Direction Commerciale** | *"Timeouts au-delà de 90 jours"*<br/>Impossible d'extraire l'historique annuel. |
| **Conformité DPO / RGPD** | *"Droit à l'oubli inapplicable"*<br/>La suppression d'un utilisateur échoue. |
| **Direction Financière** | *"Factures d'infra en flèche"*<br/>Upgrades continus du CPU/RAM sans résoudre les lenteurs. |

---

## 🛠️ Atelier Pratique : L'Audit Technique Post-Mortem
**Rôle :** Vous êtes  mandaté pour proposez des solutions aux problèmes de la plateforme.  
**Format :** En binôme | 
**Methode :** phase investigation + retour en débriefing collectif.  
**Compétence visée :** Diagnostic des risques et identification des contraintes techniques.

---

<!-- SLIDE SUIVANTE : DÉBRIEFING FORMATEUR -->

## 🔍 Débriefing de l'Audit : Le Diagnostic d'Architecture

Voici ce que l'audit technique révèle : le problème n'est pas le code, **c'est le modèle architectural**.

| Pôle | Diagnostic Technique  |
|---|---|
| **1. BI / Marketing** | **Conflit OLTP vs OLAP :** Une base relationnelle n'est pas faite pour mixer transactions ultra-rapides et gros calculs d'agrégation. Les rapports posent des **verrous de lecture (Read Locks)** et saturent le pool de connexions, bloquant les écritures d'achats. |
| **2. Commercial** | **Absence de partitionnement (Full Table Scan) :** La table grossit indéfiniment. Sans partitionnement temporel ni base analytique dédiée, le moteur charge des giga-octets de données en mémoire pour une simple moyenne annuelle. |

---
| Pôle | Diagnostic Technique  |
|---|---|
| **3. RGPD / DPO** | **Couplage fort & Intégrité référentielle rigide :** Les clés étrangères bloquent les suppressions (on ne peut pas effacer un user s'il est lié à des factures comptables). Il manque une séparation claire entre *Données d'identité* et *Événements d'achats anonymisés*. |
| **4. Finance** | **Le mur du Scale-Up (Scaling Vertical) :** Ajouter du CPU/RAM ne sert à rien si le goulot d'étranglement est la vitesse d'I/O du disque ou la contention des verrous. Il faut **distribuer (Scale-Out)**, pas grossir la machine. |


> 🚀 **Conclusion de l'audit :**  
> Pour résoudre ces 4 crises, **on ne va pas réécrire le code SQL**, on va **découpler l'architecture** grâce aux services managés de Google Cloud Platform.

---

## ⚡ 1. Incompatibilité OLTP vs OLAP & Conflits de Verrous

Pourquoi le site freeze quand le marketing lance son reporting ?

| Dimension | OLTP (Online Transaction Processing) | OLAP (Online Analytical Processing) |
|---|---|---|
| **Mission** | Enregistrer l'instant présent (*Panier, Achat*) | Analyser l'histoire (*KPIs, Bilan annuel*) |
| **Opérations** | Petits `INSERT`, `UPDATE` ciblés (par ID) | Gros `SELECT` avec `SUM`, `AVG`, `GROUP BY` |
| **Volumes & Latence** | 1 à 10 lignes à la fois \| *< 10 ms* | Millions de lignes scannées \| *Plusieurs secondes* |

---

### Le Conflit de Verrous (*Lock Contention*)
- PostgreSQL protège la cohérence avec des verrous : `AccessShareLock` (lecture) vs `RowExclusiveLock` (écriture).
- Un long calcul analytique maintient ses verrous et mobilise les workers du pool.
- Les requêtes transactionnelles rapides de paniers se retrouvent **bloquées en file d'attente** (*Wait queue*) jusqu'à l'expiration du client : **`504 Gateway Timeout`**.

---

## 🔍 2. Full Table Scan & Le Mur du Scale-Up

Pourquoi les requêtes > 90 jours plantent-elles malgré une machine surdimensionnée ?

### Le Parcours de Table Complet (*Full Table Scan / Seq Scan*)
- Les index relationnels (B-Tree) sont optimisés pour chercher une clé précise (`id = 42`), pas pour agréger des millions de dates.
- Sans **partitionnement**, PostgreSQL lit **l'intégralité des blocs du disque** un par un.
- Conséquence : le cache mémoire RAM (*Buffer Pool*) est vidé pour charger l'historique froid, ralentissant immédiatement toutes les autres requêtes du site.

---

### Le Mur de la Scalabilité Verticale (*Scale-Up*)
- **Augmenter la taille du serveur (CPU / RAM)** a des rendements décroissants :
  1. La RAM supplémentaire ne supprime ni les **conflits de verrous**, ni les attentes d'I/O disque.
  2. Le coût d'une instance géante augmente de manière exponentielle.
- 👉 **Règle d'or :** Pour l'analytique, on ne grossit pas la machine, on **découple le stockage et le calcul (*Scale-Out*)**.

---

## 🔗 3. Clés Étrangères, Intégrité Référentielle & RGPD

Pourquoi la suppression d'un compte client est-elle devenue impossible ?

### Le Piège du Couplage Fort Relationnel
- Dans le monolithe : `orders.user_id` est lié par une contrainte stricte à `users.id`.
- Un simple `DELETE FROM users WHERE id = 12` échoue avec une erreur de violation de clé étrangère (`foreign key constraint violation`).

```
  [ Table USERS ]  ◄──── Clé Étrangère Rigide ────  [ Table ORDERS ]
  (Nom, Email, PII)                                  (Comptabilité, Factures)
         │                                                      │
  Doit être effacé (RGPD)                              Obligation légale 10 ans
```

---

### La Contradiction Juridique & Technique
- **Droit à l'oubli (RGPD Art. 17) :** L'utilisateur a le droit de supprimer ses données personnelles.
- **Code de commerce :** Les factures et commandes doivent être conservées **10 ans**.
- 👉 **Solution d'Architecte :** Casser la clé étrangère en base, **pseudonymiser l'identifiant** et séparer l'identité du fait d'achat.
