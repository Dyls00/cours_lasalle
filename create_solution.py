import json
import os

exam_path = '/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/08_capstone_eda_thelook.ipynb'
sol_dir = '/Users/macbook/Development/cours_lasalle/data_manipulation/02_notebooks/solutions'
os.makedirs(sol_dir, exist_ok=True)
sol_path = os.path.join(sol_dir, '08_capstone_eda_thelook_solution.ipynb')

with open(exam_path, 'r') as f:
    nb = json.load(f)

# Define solutions mapping by checking content of cell to be robust
solutions = {
    "# 1. Chargez le dataset": [
        "# 1. Chargez le dataset\n",
        "df = pd.read_csv('../01_data/capstone/thelook_capstone.csv')\n",
        "df.head()"
    ],
    "# 2. Affichez les infos générales": [
        "# 2. Affichez les infos générales (lignes, colonnes, types)\n",
        "print(\"Forme du dataset :\", df.shape)\n",
        "display(df.info())"
    ],
    "> ✍️ **Interprétation (Markdown) :**": [
        "> ✍️ **Interprétation (Markdown) :**\n",
        "> - La colonne `created_at` est reconnue comme `object` (texte) alors que ce devrait être une date.\n",
        "> - La colonne `cost` est aussi en `object` à cause du symbole `$`, ce qui bloque les calculs mathématiques.\n",
        "> - On observe que des colonnes comme `age`, `sale_price` et `delivered_at` n'ont pas 100% de données non-nulles, il y a donc des valeurs manquantes (NaN)."
    ],
    "# 3. Défi NumPy": [
        "# 3. Défi NumPy : Extrayez la colonne 'age' sous forme de tableau NumPy.\n",
        "age_array = df['age'].to_numpy()\n",
        "\n",
        "# Utilisez NumPy pour calculer la moyenne et l'écart-type de l'âge\n",
        "moyenne_age = np.nanmean(age_array)\n",
        "ecart_type_age = np.nanstd(age_array)\n",
        "\n",
        "print(f\"Moyenne d'âge : {moyenne_age:.2f} ans\")\n",
        "print(f\"Écart-type : {ecart_type_age:.2f} ans\")"
    ],
    "# Identifiez le pourcentage de valeurs manquantes par colonne": [
        "# Identifiez le pourcentage de valeurs manquantes par colonne\n",
        "missing_pct = (df.isna().mean() * 100).sort_values(ascending=False)\n",
        "missing_pct[missing_pct > 0]"
    ],
    "> ✍️ **Vos choix d'imputation :**": [
        "> ✍️ **Vos choix d'imputation :**\n",
        "> - **`age`** et **`sale_price`** : On va remplacer les valeurs manquantes par la **médiane**, car la moyenne est trop sensible aux éventuels âges à 120 ans ou prix démesurés (outliers).\n",
        "> - **`delivered_at`** : On laisse les NaN ! Si la date de livraison manque, cela signifie fort probablement que la commande est en transit ou annulée. Remplacer par une fausse date fausserait l'analyse des délais de livraison."
    ],
    "# Appliquez vos stratégies de traitement des NaN": [
        "# Appliquez vos stratégies de traitement des NaN\n",
        "df['age'] = df['age'].fillna(df['age'].median())\n",
        "df['sale_price'] = df['sale_price'].fillna(df['sale_price'].median())\n",
        "\n",
        "print(\"NaN restants pour age :\", df['age'].isna().sum())\n",
        "print(\"NaN restants pour sale_price :\", df['sale_price'].isna().sum())"
    ],
    "# Détectez et supprimez les doublons exacts": [
        "# Détectez et supprimez les doublons exacts\n",
        "nb_doublons = df.duplicated().sum()\n",
        "print(f\"Nombre de doublons avant nettoyage : {nb_doublons}\")\n",
        "\n",
        "df = df.drop_duplicates()\n",
        "print(f\"Nombre de doublons après nettoyage : {df.duplicated().sum()}\")"
    ],
    "# Corrigez la colonne 'cost'": [
        "# Corrigez la colonne 'cost' (qui contient actuellement du texte avec le symbole '$') pour la transformer en Float\n",
        "df['cost'] = df['cost'].str.replace('$', '', regex=False).astype(float)\n",
        "print(\"Nouveau type de cost :\", df['cost'].dtype)"
    ],
    "# Convertissez 'created_at' en format datetime": [
        "# Convertissez 'created_at' en format datetime\n",
        "df['created_at'] = pd.to_datetime(df['created_at'])\n",
        "print(\"Nouveau type de created_at :\", df['created_at'].dtype)"
    ],
    "# Harmonisez la colonne 'country'": [
        "# Harmonisez la colonne 'country' qui contient des fautes de frappe\n",
        "print(\"Avant harmonisation (top 10) :\\n\", df['country'].value_counts().head(10))\n",
        "\n",
        "mapping = {\n",
        "    'US': 'United States', \n",
        "    'USA': 'United States',\n",
        "    'U.S.A.': 'United States',\n",
        "    'united states': 'United States',\n",
        "    '  United States': 'United States',\n",
        "    'UK': 'United Kingdom',\n",
        "    'U.K.': 'United Kingdom'\n",
        "}\n",
        "df['country'] = df['country'].replace(mapping)\n",
        "\n",
        "print(\"\\nAprès harmonisation :\\n\", df['country'].value_counts().head(10))"
    ],
    "# Gérez les valeurs aberrantes": [
        "# Gérez les valeurs aberrantes (outliers) dans 'sale_price'\n",
        "print(\"Statistiques de sale_price avant :\\n\", df['sale_price'].describe())\n",
        "\n",
        "# On garde uniquement les prix strictement positifs et on plafonne par exemple à 2000 (ou on filtre)\n",
        "df = df[(df['sale_price'] > 0) & (df['sale_price'] < 5000)]\n",
        "\n",
        "# Même chose pour l'âge (pas plus de 120 ans)\n",
        "df = df[df['age'] <= 120]\n",
        "\n",
        "print(\"\\nStatistiques de sale_price après :\\n\", df['sale_price'].describe())"
    ],
    "# 1. Créez une colonne 'marge'": [
        "# 1. Créez une colonne 'marge' = sale_price - cost\n",
        "df['marge'] = df['sale_price'] - df['cost']"
    ],
    "# 2. Créez une colonne 'taux_marge_pct'": [
        "# 2. Créez une colonne 'taux_marge_pct' = (marge / sale_price) * 100\n",
        "df['taux_marge_pct'] = (df['marge'] / df['sale_price']) * 100"
    ],
    "# 3. Extrayez le 'mois'": [
        "# 3. Extrayez le 'mois' et le 'jour_semaine' à partir de 'created_at'\n",
        "df['mois'] = df['created_at'].dt.month\n",
        "df['jour_semaine'] = df['created_at'].dt.day_name()"
    ],
    "# 4. Créez une colonne 'tranche_age'": [
        "# 4. Créez une colonne 'tranche_age' catégorisant l'âge des clients\n",
        "# bins : [0, 25, 35, 50, 150]\n",
        "df['tranche_age'] = pd.cut(\n",
        "    df['age'], \n",
        "    bins=[0, 25, 35, 50, 150], \n",
        "    labels=['18-25', '26-35', '36-50', '50+']\n",
        ")\n",
        "df['tranche_age'].value_counts()"
    ],
    "# Question Business 1 : Quelle est la répartition": [
        "# Question Business 1 : Quelle est la répartition des ventes par pays (le Top 5) ?\n",
        "top_countries = df['country'].value_counts().head(5)\n",
        "print(top_countries)\n",
        "\n",
        "top_countries.plot(kind='bar', color='coral', figsize=(8, 4))\n",
        "plt.title('Top 5 des pays par volume de ventes')\n",
        "plt.ylabel('Nombre de ventes')\n",
        "plt.xticks(rotation=45)\n",
        "plt.show()"
    ],
    "# Question Business 2 : La plateforme attire-t-elle": [
        "# Question Business 2 : La plateforme attire-t-elle plus une clientèle jeune (18-35 ans) ou âgée (36+) ?\n",
        "repartition_age = df['tranche_age'].value_counts(normalize=True) * 100\n",
        "print(repartition_age.round(1))\n",
        "\n",
        "repartition_age.plot(kind='pie', autopct='%1.1f%%', figsize=(5, 5), colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])\n",
        "plt.title('Répartition de la clientèle par tranche d\\'âge')\n",
        "plt.ylabel('')\n",
        "plt.show()\n",
        "# -> L'audience est relativement équilibrée, avec une prédominance légère pour les jeunes / jeunes actifs."
    ],
    "# Question Business 3 : Y a-t-il une différence": [
        "# Question Business 3 : Y a-t-il une différence de prix d'achat moyen entre les produits 'Women' et 'Men' ?\n",
        "# Hypothèse : la colonne est 'department'\n",
        "if 'department' in df.columns:\n",
        "    mean_price_dept = df.groupby('department')['sale_price'].mean()\n",
        "    print(mean_price_dept)\n",
        "    \n",
        "    mean_price_dept.plot(kind='bar', color=['blue', 'pink'], figsize=(6, 4))\n",
        "    plt.title('Prix moyen de vente par département')\n",
        "    plt.ylabel('Prix de vente moyen ($)')\n",
        "    plt.xticks(rotation=0)\n",
        "    plt.show()\n",
        "else:\n",
        "    print(\"La colonne 'department' n'est pas présente dans ce dataset.\")"
    ],
    "> 1. **Insight 1 :** ...": [
        "> 1. **Insight 1 :** **Problème de Qualité de Données** - Notre système de collecte a un problème. Nous avons des doublons de commandes, des âges aberrants (> 120 ans) et des prix de revient (cost) enregistrés comme texte avec des `$`, ce qui fausse nos calculs automatiques. Il faut remonter cela à l'équipe Data Engineering.\n",
        "> \n",
        "> 2. **Insight 2 :** **Marché cible (Géographie)** - Les États-Unis sont notre marché dominant de très loin. Une opportunité serait soit de consolider notre force de frappe là-bas, soit d'enquêter sur les raisons de notre sous-performance en Europe (Royaume-Uni, France) : est-ce lié aux frais de livraison ?\n",
        "> \n",
        "> 3. **Insight 3 :** **Profil Démographique** - Nous n'avons pas qu'une clientèle \"jeune\". Les 36-50 ans représentent une part énorme de notre base. Or, le marketing TheLook est souvent tourné vers les 18-25 ans. Il faudrait adapter nos campagnes pour fidéliser ce segment plus âgé qui a probablement un pouvoir d'achat supérieur."
    ]
}

# Update cells
for cell in nb['cells']:
    src_str = ''.join(cell['source'])
    for key, sol_lines in solutions.items():
        if key in src_str:
            cell['source'] = sol_lines

# Update first title
nb['cells'][0]['source'] = [
    "# 🟢 CORRECTION DE L'EXAMEN : Analyse Exploratoire de TheLook eCommerce\n",
    "\n",
    "Ce notebook contient la correction détaillée de l'examen final. \n",
    "Prenez le temps de lire les cellules markdown et les commentaires dans le code pour comprendre la démarche."
]

with open(sol_path, 'w') as f:
    json.dump(nb, f, indent=1)

print(f"Solution generated at {sol_path}")
