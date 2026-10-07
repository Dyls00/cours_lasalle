import json
import os
import shutil

nb_dir = '/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks'

# 1. Rename files
def safe_rename(old, new):
    if os.path.exists(os.path.join(nb_dir, old)):
        shutil.move(os.path.join(nb_dir, old), os.path.join(nb_dir, new))

safe_rename('04_exercice_integrateur.ipynb', '05_exercice_integrateur.ipynb')
safe_rename('05_nettoyage_donnees.ipynb', '04_nettoyage_donnees.ipynb')

os.makedirs(os.path.join(nb_dir, 'Bonus'), exist_ok=True)
safe_rename('06_agregation_groupby_pivots.ipynb', 'Bonus/06_agregation_groupby_pivots.ipynb')
safe_rename('07_complements_merge_export_viz.ipynb', 'Bonus/07_complements_merge_export_viz.ipynb')

# 2. Patch 05_exercice_integrateur.ipynb
nb5_path = os.path.join(nb_dir, '05_exercice_integrateur.ipynb')
if os.path.exists(nb5_path):
    with open(nb5_path, 'r') as f:
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

    # Use a dirty dataset
    for i, c in enumerate(nb['cells']):
        src = ''.join(c['source'])
        if "pd.\"FONCTION\"" in src:
            nb['cells'][i]['source'] = [
                "# Chargez le dataset (utilisez la version 'dirty' pour vous entraîner au nettoyage)\n",
                "sales = pd.read_csv('../01_data/exercises/thelook_sales_dirty.csv')"
            ]
            # insert the cleaning cells 3 cells after the load cell (which is around index 3)
            # Find the "## Étape 2" markdown index
            idx_etape_2 = next((j for j, cell in enumerate(nb['cells']) if "## Étape 2" in ''.join(cell['source'])), None)
            if idx_etape_2:
                nb['cells'] = nb['cells'][:idx_etape_2] + cleaning_cells + nb['cells'][idx_etape_2:]
            break

    with open(nb5_path, 'w') as f:
        json.dump(nb, f, indent=1)


# 3. Patch 08_capstone_eda_thelook.ipynb
nb8_path = os.path.join(nb_dir, '08_capstone_eda_thelook.ipynb')
if os.path.exists(nb8_path):
    with open(nb8_path, 'r') as f:
        nb = json.load(f)
    
    nb['cells'][0]['source'] = [
        "# 🚀 EXAMEN : Projet Capstone — Analyse Exploratoire de TheLook eCommerce\n",
        "\n",
        "**Durée : 2h30 (incluant une pause libre de 15 minutes), suivi de soutenances orales.**\n",
        "\n",
        "Vous recevez un dataset brut et dénormalisé de TheLook. Votre mission : mener une EDA complète, du chargement aux insights, de manière autonome.\n",
        "Documentez TOUT dans des cellules Markdown. Ce notebook constituera votre livrable d'examen."
    ]
    with open(nb8_path, 'w') as f:
        json.dump(nb, f, indent=1)

