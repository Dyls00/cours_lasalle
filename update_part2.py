import json

file_path = "big_data/02_cours/day2_transformation/labs/01_lab_medallion_bases.ipynb"
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_source = [
    "## Partie 2 : Vue ou Table Matérialisée ?\n",
    "\n",
    "Avant de créer notre vue, faisons un court rappel théorique sur les différences entre une **Vue standard** et une **Vue matérialisée** dans BigQuery :\n",
    "\n",
    "| Caractéristique | Vue standard (`CREATE VIEW`) | Vue matérialisée (`CREATE MATERIALIZED VIEW`) |\n",
    "| :--- | :--- | :--- |\n",
    "| **Stockage** | Aucun (c'est juste une requête sauvegardée) | Stocke physiquement les résultats pré-calculés |\n",
    "| **Coût de facturation** | Scan total des tables sous-jacentes à chaque fois | Réduit (lit les données pré-calculées + le delta récent) |\n",
    "| **Performance** | Plus lent (recalcule tout à la volée) | Très rapide (zéro-maintenance, cache intelligent) |\n",
    "| **Mise à jour** | Toujours 100% en temps réel | Automatique en arrière-plan (BigQuery gère le rafraîchissement) |\n",
    "| **Cas d'usage idéal** | Logique métier de base (Silver), restriction d'accès | Tableaux de bord (Gold), agrégations coûteuses appelées souvent |\n",
    "\n",
    "---\n",
    "Au lieu d'une table physique qui doit être recalculée manuellement, on peut créer une vue matérialisée pour la couche Silver, ou une vue simple pour des requêtes de préparation.\n",
    "\n",
    "**Exemple de Vue Matérialisée :**\n",
    "```sql\n",
    "CREATE MATERIALIZED VIEW `thelook_prenom.silver_mv_shipped_orders` AS\n",
    "SELECT order_id, user_id FROM `thelook_prenom.bronze_raw_orders_items` WHERE status = 'Shipped';\n",
    "```"
]

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown' and cell['source'] and cell['source'][0].startswith("## Partie 2 : Vue ou Table"):
        cell['source'] = new_source
        break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write("\n")

print("Partie 2 updated with the markdown table!")
