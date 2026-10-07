import json

with open('/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/05_exercice_integrateur.ipynb', 'r') as f:
    nb = json.load(f)

# Modify intro note
nb['cells'][0]['source'] = [
    "# 🏋️ Exercice Intégrateur — L'Analyste Junior (Préparation Examen)\n",
    "\n",
    "Vous venez d'être embauché(e) comme Junior Data Analyst chez TheLook, une boutique de mode en ligne.\n",
    "Votre manager vous confie un premier fichier de ventes et attend un rapport d'exploration complet.\n",
    "\n",
    "> 💡 **Note:** Cet exercice est la version guidée et concentrée de ce qui vous attend cet après-midi pour votre projet final (qui servira d'examen). \n",
    "> Profitez de cette session (1h15) pour valider vos acquis : chargement, exploration, **nettoyage**, filtrage, transformation et statistiques descriptives."
]

# Insert step 1.5 Nettoyage after step 1
# Current step 1 cells are indices 2 to 6 (markdown, load, shape, types, nans)
# So at index 7, we'll insert Nettoyage
cleaning_cells = [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Étape 1.5 : Nettoyer les données\n",
    "Votre exploration a révélé des problèmes. Avant de faire des statistiques, il faut s'assurer que les données sont propres."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Traitez les valeurs manquantes (imputez ou supprimez en justifiant votre choix en commentaire)\n",
    "# Votre code ici"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Vérifiez et supprimez les doublons exacts s'il y en a\n",
    "# Votre code ici"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Standardisez une colonne texte (ex: mettez les noms de pays en minuscules et sans espaces autour pour vérifier la propreté)\n",
    "# Votre code ici"
   ]
  }
]

# Use a clean dataset for this exercise or the dirty one?
# In the original, it loads `thelook_sales.csv`. 
# To make it meaningful, we should ask them to load `thelook_sales_dirty.csv` instead.
nb['cells'][3]['source'] = [
    "# Chargez le dataset (utilisez la version 'dirty' pour vous entraîner au nettoyage)\n",
    "# '../01_data/exercises/thelook_sales_dirty.csv'\n",
    "sales = "
]

# Insert cleaning cells
new_cells = nb['cells'][:7] + cleaning_cells + nb['cells'][7:]

nb['cells'] = new_cells

with open('/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/05_exercice_integrateur.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("Notebook 05 successfully patched!")
