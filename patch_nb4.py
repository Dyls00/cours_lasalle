import json
import os

nb4_path = '/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/04_nettoyage_donnees.ipynb'
with open(nb4_path, 'r') as f:
    nb = json.load(f)

# The replace vs map should be added in Section 5, before the "Nettoyer la casse avec .str"
# Let's find the cell containing "### Recoder avec .map()"
map_idx = next((i for i, c in enumerate(nb['cells']) if "### Recoder avec .map()" in ''.join(c['source'])), None)

if map_idx is not None:
    diff_cells = [
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": [
        "### ⚖️ Différence clé : `.replace()` vs `.map()`\n",
        "\n",
        "La différence majeure réside dans le comportement face aux **valeurs qui NE sont PAS dans le dictionnaire** :\n",
        "\n",
        "| Méthode | Ce qu'elle fait aux valeurs absentes du dictionnaire | Utilisation idéale |\n",
        "| :--- | :--- | :--- |\n",
        "| **`.replace()`** | **Conserve les valeurs d'origine intactes** | **Nettoyage ponctuel** : corriger quelques fautes de frappe sans toucher au reste des données. |\n",
        "| **`.map()`** | **Les transforme toutes en `NaN` !** | **Recodage exhaustif** : quand toutes les catégories possibles sont connues à 100%. |\n",
        "\n",
        "#### 🧪 Exemple illustratif :"
       ]
      },
      {
       "cell_type": "code",
       "execution_count": None,
       "metadata": {},
       "outputs": [],
       "source": [
        "# Imaginons la série suivante :\n",
        "s = pd.Series(['US', 'France', 'spain'])\n",
        "mapping = {'US': 'United States', 'spain': 'Spain'}"
       ]
      },
      {
       "cell_type": "code",
       "execution_count": None,
       "metadata": {},
       "outputs": [],
       "source": [
        "s.replace(mapping)\n",
        "# Résultat :\n",
        "# 0    United States\n",
        "# 1           France   <-- 'France' est CONSERVÉ intact !\n",
        "# 2            Spain\n"
       ]
      },
      {
       "cell_type": "code",
       "execution_count": None,
       "metadata": {},
       "outputs": [],
       "source": [
        "s.map(mapping)\n",
        "# Résultat :\n",
        "# 0    United States\n",
        "# 1              NaN   <-- ATTENTION : 'France' est devenu NaN car absent du dictionnaire !\n",
        "# 2            Spain\n"
       ]
      }
    ]
    # Insert right after the map() example, which is map_idx + 2
    insert_idx = map_idx + 2
    nb['cells'] = nb['cells'][:insert_idx] + diff_cells + nb['cells'][insert_idx:]

with open(nb4_path, 'w') as f:
    json.dump(nb, f, indent=1)

