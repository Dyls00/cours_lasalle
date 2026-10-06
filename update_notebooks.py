import json

def update_nb5():
    with open('/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/05_exercice_integrateur.ipynb', 'r') as f:
        nb = json.load(f)
    
    # Update first cell
    cell = nb['cells'][0]
    cell['source'] = [
        "# 🏋️ Exercice Intégrateur — L'Analyste Junior (Préparation Examen)\n",
        "\n",
        "Vous venez d'être embauché(e) comme Junior Data Analyst chez TheLook, une boutique de mode en ligne.\n",
        "Votre manager vous confie un premier fichier de ventes et attend un rapport d'exploration complet.\n",
        "\n",
        "> 💡 **Note du formateur :** Cet exercice est le \"Papa\" (la version guidée et concentrée) de ce qui vous attend cet après-midi pour votre projet final (qui servira d'examen). \n",
        "> Profitez de cette session (1h15) pour valider vos acquis : chargement, exploration, filtrage, transformation et statistiques descriptives."
    ]
    
    with open('/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/05_exercice_integrateur.ipynb', 'w') as f:
        json.dump(nb, f, indent=1)

def update_nb8():
    with open('/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/08_capstone_eda_thelook.ipynb', 'r') as f:
        nb = json.load(f)
    
    # Update first cell
    cell = nb['cells'][0]
    cell['source'] = [
        "# 🚀 EXAMEN : Projet Capstone — Analyse Exploratoire de TheLook eCommerce\n",
        "\n",
        "**Durée : 2h30 (incluant une pause libre de 15 minutes), suivi de soutenances orales.**\n",
        "\n",
        "Vous recevez un dataset brut et dénormalisé de TheLook. Votre mission : mener une EDA complète, du chargement aux insights, de manière autonome.\n",
        "Documentez TOUT dans des cellules Markdown. Ce notebook constituera votre livrable d'examen."
    ]
    
    with open('/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/08_capstone_eda_thelook.ipynb', 'w') as f:
        json.dump(nb, f, indent=1)

update_nb5()
update_nb8()
print("Notebooks updated successfully.")
