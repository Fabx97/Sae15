import pandas as pd
import folium
import matplotlib.pyplot as plt

# Configuration de l'affichage
plt.style.use('seaborn-v0_8-darkgrid')
pd.set_option('display.max_rows', 20)

#Exportation du fichier
fichier = "experimentations_5G.csv"
donnees = pd.read_csv(fichier, encoding="cp1252", sep=";")


print(f"{len(donnees)} sites chargés")
print("\nPremières lignes :")
print(donnees.head(3))


# Nettoyage
print("\nNettoyage des données")


# Standardisation des noms de colonnes
donnees.columns = [col.strip().lower().replace(" ", "_") for col in donnees.columns]


# Convertir les coordonnées (remplacer virgules par points)
donnees["latitude"] = donnees["latitude"].astype(str).str.replace(",", ".").astype(float)
donnees["longitude"] = donnees["longitude"].astype(str).str.replace(",", ".").astype(float)


# Garde uniquement les sites avec coordonnées GPS valides
avant = len(donnees)
donnees = donnees.dropna(subset=["latitude", "longitude"])
apres = len(donnees)


print(f"{avant - apres} sites sans coordonnées supprimés")
print(f"{apres} sites valides conservés\n")


# ANALYSE
print("Analyse des expérimentations\n")


# Par région
sites_par_region = donnees["région"].value_counts()
print("Top 5 des régions :")
for region, nb in sites_par_region.head(5).items():
    print(f" {region}: {nb} sites")


# Par acteur
sites_par_acteur = donnees["expérimentateur"].value_counts()
print("\nTop 5 des acteurs :")
for acteur, nb in sites_par_acteur.head(5).items():
    print(f" {acteur}: {nb} expérimentations")


# GRAPHIQUE
print("\nCréation des graphiques...")


# Graphique des régions
fig, ax = plt.subplots(figsize=(12, 6))
sites_par_region.plot(kind='barh', ax=ax, color='steelblue')
ax.set_title("Expérimentations 5G par région", fontsize=16, fontweight='bold')
ax.set_xlabel("Nombre de sites", fontsize=12)
ax.set_ylabel("")
plt.tight_layout()
plt.savefig("bilan_regions.png", dpi=150)
print("Graphique régions sauvegardé")
plt.close()


# Graphique des acteurs
fig, ax = plt.subplots(figsize=(12, 6))
sites_par_acteur.head(10).plot(kind='barh', ax=ax, color='coral')
ax.set_title("Top 10 des acteurs", fontsize=16, fontweight='bold')
ax.set_xlabel("Nombre d'expérimentations", fontsize=12)
ax.set_ylabel("")
plt.tight_layout()
plt.savefig("bilan_acteurs.png", dpi=150)
print("Graphique acteurs sauvegardé")
plt.close()


#  CARTE INTERACTIVE
print("\nGénération de la carte interactive...")


# Centre de la France
carte = folium.Map(location=[46.6, 2.5], zoom_start=6)


# Ajout des marqueurs
for _, site in donnees.iterrows():
    info = f"""
    <div style="font-family: Arial; font-size: 12px;">
        <b>{site['expérimentateur']}</b><br>
         {site['commune']} ({site['région']})<br>
        {site['bande_de_fréquences']}
    </div>
    """

    folium.Marker(
        location=[site['latitude'], site['longitude']],
        popup=folium.Popup(info, max_width=300),
        tooltip=site['commune'],
        icon=folium.Icon(color='blue', icon='signal', prefix='fa')
    ).add_to(carte)


carte.save("carte_5G.html")
print("Carte sauvegardée : carte_5G.html")


# PAGE HTML DE RÉPERTOIRE

# Récupérer les colonnes de technologies (colonnes 16 à 33)
colonnes_tech = donnees.columns[16:34].tolist()


# Fonction pour extraire les technologies actives
def obtenir_technologies(row):
    techs = []
    for col in colonnes_tech:
        if col in row.index and str(row[col]).lower() in ['true', '1', 'oui', 'yes']:
            tech_name = col.replace('_', ' ').title()
            techs.append(tech_name)
    return ', '.join(techs) if techs else 'Non spécifié'


# HTML
html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Répertoire 5G</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
        }

        h1 {
            font-size: 24px;
            margin-bottom: 10px;
            color: #333;
        }
       
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
       
        .stats {
            display: flex;
            gap: 30px;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #ddd;
        }
       
        .stat {
            text-align: center;
        }
       
        .stat-value {
            font-size: 28px;
            font-weight: bold;
            color: #333;
        }
       
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
       
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
       
        th {
            background: #f0f0f0;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            color: #333;
            border-bottom: 2px solid #ddd;
        }
       
        td {
            padding: 12px;
            border-bottom: 1px solid #eee;
            font-size: 13px;
        }
       
        tr:hover {
            background: #fafafa;
        }
       
        .tech-list {
            color: #666;
        }
       
        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #999;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Répertoire des Expérimentations 5G</h1>
        <p class="subtitle">Liste complète des sites, acteurs et technologies déployées</p>
       
        <div class="stats">
            <div class="stat">
                <div class="stat-value">""" + str(len(donnees)) + """</div>
                <div class="stat-label">Sites</div>
            </div>
            <div class="stat">
                <div class="stat-value">""" + str(donnees['région'].nunique()) + """</div>
                <div class="stat-label">Régions</div>
            </div>
            <div class="stat">
                <div class="stat-value">""" + str(donnees['expérimentateur'].nunique()) + """</div>
                <div class="stat-label">Acteurs</div>
            </div>
            <div class="stat">
                <div class="stat-value">""" + str(donnees['bande_de_fréquences'].nunique()) + """</div>
                <div class="stat-label">Fréquences</div>
            </div>
        </div>
       
        <table>
            <thead>
                <tr>
                    <th>Région</th>
                    <th>Commune</th>
                    <th>Acteur</th>
                    <th>Fréquence</th>
                    <th>Technologies</th>
                </tr>
            </thead>
            <tbody>
"""


# Ajouter les lignes de données
for _, site in donnees.iterrows():
    technologies = obtenir_technologies(site)
    html_content += f"""<tr>
                    <td>{site['région']}</td>
                    <td>{site['commune']}</td>
                    <td>{site['expérimentateur']}</td>
                    <td>{site['bande_de_fréquences']}</td>
                    <td class="tech-list">{technologies}</td>
                </tr>
"""


html_content += """            </tbody>
        </table>
       
        <footer>
            Analyse 5G - """ + str(len(donnees)) + """ sites répertoriés
        </footer>
    </div>
</body>
</html>
"""


# Sauvegarde fichier HTML
with open("repertoire_5G.html", "w", encoding="utf-8") as f:
    f.write(html_content)


print("Répertoire HTML sauvegardé : repertoire_5G.html")


# RÉSUMÉ FINAL
print("\n" + "="*50)
print("RÉSUMÉ")
print("="*50)
print(f"Total de sites analysés : {len(donnees)}")
print(f"Nombre de régions : {donnees['région'].nunique()}")
print(f"Nombre d'acteurs : {donnees['expérimentateur'].nunique()}")
print(f"\nRégion la plus active : {sites_par_region.index[0]}")
print(f"Acteur le plus actif : {sites_par_acteur.index[0]}")
print("="*50)
