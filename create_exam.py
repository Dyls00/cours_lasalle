import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🚀 EXAMEN FINAL : Analyse Exploratoire de TheLook eCommerce\n",
    "\n",
    "**Durée :** 2h30 (incluant une pause libre de 15 minutes), suivi de soutenances orales.\n",
    "\n",
    "---\n",
    "## ⚖️ Modalités d'Évaluation (IMPORTANT)\n",
    "La note finale est divisée en deux parties égales (50% / 50%) :\n",
    "\n",
    "### 1. La Soutenance Orale (50% de la note) 🗣️\n",
    "Les critères les plus importants de cet examen ne sont pas seulement techniques. Nous évaluerons :\n",
    "- **La structuration de votre analyse** : votre démarche a-t-elle du sens ?\n",
    "- **L'explication de vos choix** : *pourquoi* avez-vous imputé cette donnée ? *pourquoi* avez-vous filtré ainsi ?\n",
    "- **L'organisation de votre Notebook** : utilisation pertinente du Markdown pour créer un rapport lisible (titres, paragraphes, puces).\n",
    "- **La propreté de votre code** : variables explicites, code commenté avec `#`.\n",
    "- **L'interprétation métier (Business)** : tirez des conclusions utiles pour l'entreprise.\n",
    "\n",
    "### 2. Le Livrable technique (Ce Notebook) (50% de la note) 💻\n",
    "- Validation des compétences vues lors des 4 premiers notebooks (NumPy, Pandas, Feature Engineering, Nettoyage).\n",
    "- Exécution sans erreur (le notebook doit pouvoir s'exécuter de haut en bas).\n",
    "\n",
    "---\n",
    "## 📁 À propos du Dataset\n",
    "- **Fichier :** `../01_data/capstone/thelook_capstone.csv` (~51 000 lignes)\n",
    "- Ce fichier regroupe les commandes, les utilisateurs et les produits. \n",
    "- ⚠️ **Attention :** Ce dataset est intentionnellement \"sale\". Il contient des valeurs manquantes, des types incorrects, des doublons, des fautes de frappe et des valeurs aberrantes."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import des bibliothèques nécessaires\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## 🛠️ PARTIE 1 : Chargement & Exploration Initiale (Pandas & NumPy)\n",
    "*Valide les compétences du Notebook 1 (NumPy) et Notebook 2 (Pandas Premiers Pas).*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Chargez le dataset\n",
    "df = "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. Affichez les infos générales (lignes, colonnes, types)\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "> ✍️ **Interprétation (Markdown) :** Que remarquez-vous sur les types de données actuels ? (ex: `created_at`, `cost`)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. Défi NumPy : Extrayez la colonne 'age' sous forme de tableau NumPy.\n",
    "# Utilisez NumPy pour calculer la moyenne et l'écart-type de l'âge (Attention aux NaN ! Pensez à np.nanmean / np.nanstd)\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## 🧹 PARTIE 2 : Le Nettoyage de Données (Le cœur du travail)\n",
    "*Valide les compétences du Notebook 4 (Nettoyage). Pensez à justifier vos choix !*"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.1 Les valeurs manquantes (NaN)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Identifiez le pourcentage de valeurs manquantes par colonne\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "> ✍️ **Vos choix d'imputation :** Comment allez-vous traiter les NaN dans `age`, `sale_price` et `delivered_at` ? Expliquez vos choix."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Appliquez vos stratégies de traitement des NaN\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.2 Doublons et types incorrects"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Détectez et supprimez les doublons exacts\n",
    ""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Corrigez la colonne 'cost' (qui contient actuellement du texte avec le symbole '$') pour la transformer en Float\n",
    ""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Convertissez 'created_at' en format datetime\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.3 Harmonisation (.replace ou .map) et Outliers"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Harmonisez la colonne 'country' qui contient des fautes de frappe (utilisez value_counts pour les repérer)\n",
    ""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Gérez les valeurs aberrantes (outliers) dans 'sale_price' (ex: prix négatifs ou absurdes)\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## 🏗️ PARTIE 3 : Feature Engineering & Transformations\n",
    "*Valide les compétences du Notebook 3 (Transformations).*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Créez une colonne 'marge' = sale_price - cost\n",
    ""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. Créez une colonne 'taux_marge_pct' = (marge / sale_price) * 100\n",
    ""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. Extrayez le 'mois' et le 'jour_semaine' à partir de 'created_at'\n",
    ""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 4. Créez une colonne 'tranche_age' catégorisant l'âge des clients : '18-25', '26-35', '36-50', '50+' (Utilisez pd.cut)\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## 📈 PARTIE 4 : Analyse Business & Insights\n",
    "Utilisez toutes les méthodes à votre disposition (filtrage, `.value_counts()`, statistiques basiques, `.plot()`) pour extraire de la valeur."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Question Business 1 : Quelle est la répartition des ventes par pays (le Top 5) ? (Tracez un graphique en barre)\n",
    ""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Question Business 2 : La plateforme attire-t-elle plus une clientèle jeune (18-35 ans) ou âgée (36+) ?\n",
    ""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Question Business 3 : Y a-t-il une différence de prix d'achat moyen entre les produits 'Women' et 'Men' ?\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## 🎤 PARTIE 5 : Préparation de la Soutenance (Synthèse Manager)\n",
    "\n",
    "Rédigez ci-dessous la trame de votre soutenance. Résumez vos **3 découvertes les plus importantes** pour le comité de direction de TheLook. Ne décrivez pas votre code, décrivez la réalité du business (marges, problèmes de données récurrents chez les clients, profil type d'acheteur, etc.)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "> 1. **Insight 1 :** ...\n",
    "> \n",
    "> 2. **Insight 2 :** ...\n",
    "> \n",
    "> 3. **Insight 3 :** ..."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": ".venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open('/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/08_capstone_eda_thelook.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)
