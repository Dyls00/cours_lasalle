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
- **Défis de l'OLTP sous charge analytique** : Conflits de verrous & MVCC sur PostgreSQL
- **Découplage microservices** : Du monolithe à l'architecture distribuée
- **Patrons & Outils cibles** : Dual-write vs Outbox Pattern, CDC (WAL), Datastream & Pub/Sub

---

## 🎯 Contexte & Objectifs Pédagogiques

>  **Notre mission de la semaine** : Sortir d'une vision monolithique centralisée pour concevoir une architecture data cloud résiliente et conforme aux standards industriels sur **Google Cloud Platform**.

### Objectifs d'apprentissage du Jour 1
1. **Comprendre la fracture OLTP vs OLAP** : Pourquoi mutualiser transactions et analytics détruit la production.
2. **Diagnostiquer les pannes réelles** : Observer l'utilisation des ressources, l l'invalidation de cache et le *Table Bloat*.
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
| **Direction Commerciale** | *"Timeouts au-delà de 90 jours"*<br/>Impossible d'extraire l'historique annuel (`Query Timeout`). |
| **Conformité DPO / RGPD** | *"Droit à l'oubli inapplicable"*<br/>La suppression d'un user échoue à cause des clés étrangères. |
| **Direction Financière** | *"Factures d'infra en flèche"*<br/>Upgrades continus du CPU/RAM sans résoudre les lenteurs. |

---

## 🛠️ Atelier Pratique : L'Audit Technique Post-Mortem
**Rôle :** Vous êtes  mandaté pour proposez des solutions aux problèmes de la plateforme.  
**Format :** En binôme | ⏱️ **Durée :** 20 min d'investigation + 10 min de débriefing collectif.  
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
> Pour résoudre ces 4 crises, **on ne va pas réécrire le code SQL**, on va **découpler l'architecture** grâce aux services managés de Google Cloud Platform (Cloud Run, Pub/Sub, BigQuery).

---
