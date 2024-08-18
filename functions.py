## Import packages

import streamlit as st

# NBA api endpoints
from nba_api.stats.endpoints import playerestimatedmetrics
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

#Dataviz
import matplotlib.pyplot as plt
import seaborn as sns

# Other packages
import re
import json
import numpy as np
import pandas as pd
import matplotlib.image as mpimg

# Pandas config
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Import xlsx data
true_data=pd.read_excel('./src/data_dh20.xlsx', sheet_name='Réponses individuelles')
ids=pd.read_excel('./src/dh20_ids.xlsx',sheet_name='Feuil1')

# Import DH logo

img = mpimg.imread('./src/logo-dunkhebdo.jpg')

#Fonction du graphique de votes
def vote_graph(player):

    joueur = player
    true_data_f = load_transform_data(true_data)
    df_joueur = true_data_f[[joueur, 'Editorial_Member']].dropna()

    # Calculer la moyenne globale des notes
    moyenne_globale = df_joueur[joueur].mean()

    # Séparer les membres de la rédaction et les autres
    df_editorial = df_joueur[df_joueur['Editorial_Member']]
    df_non_editorial = df_joueur[~df_joueur['Editorial_Member']]

    # Créer une figure et des axes
    fig, ax = plt.subplots(figsize=(12, 8))

    # Créer un violon plot en excluant les membres de la rédaction
    sns.violinplot(x='Editorial_Member', y=joueur, data=df_non_editorial, inner='quartile', color='lightgray', ax=ax, label="Communauté DH")

    # Ajouter un swarm plot pour les membres de la rédaction
    sns.swarmplot(x='Editorial_Member', y=joueur, data=df_editorial, color='blue', ax=ax, label='Rédaction DH')

    # Ajouter une ligne pour la moyenne globale
    ax.axhline(y=moyenne_globale, color='red', linestyle='--', label='Moyenne Globale')

    # Inverser l'axe y
    ax.invert_yaxis()

    # Dictionnaire des labels
    labels = {i: str(i) for i in range(1, 22)}
    labels[22] = "Non classé"

    # Remplacer les valeurs numériques par des étiquettes textuelles sur l'axe y
    ax.set_yticks(list(range(1, 23)))
    ax.set_yticklabels([labels.get(i, i) for i in range(1, 23)])

    # Ajuster les limites de l'axe y
    ax.set_ylim(22.5, 0.5)  # Ajuster les limites pour correspondre à l'inversion de l'axe
    ax.set_xlim(-1, 1)

    # Retirer les labels et les ticks de l'axe x
    ax.set_xlabel('')  # Retirer le label de l'axe x
    ax.set_xticks([])   # Retirer les ticks de l'axe x

    # Ajouter un titre et des labels
    ax.set_title(f'Répartition des notes : {joueur}')
    ax.set_ylabel('Note')

    # Ajouter une légende manuelle
    handles, labels = ax.get_legend_handles_labels()
    # Ajouter le handle du violin plot
    handles.append(plt.Line2D([0], [0], color='lightgray', lw=4))

    ax.legend(handles=handles, labels=labels)
    ax.imshow(img, interpolation='nearest', extent=[-0.95, -0.5, 1, 5], aspect='auto', alpha=1)

    # Afficher le plot
    st.pyplot(fig)

## Function to get team id from the abbreviation
def get_player_id(name) :
    player_id=ids[ids["player_nickname"]==name].reset_index()["player_id"][0]
    return player_id

# Fonction de chargement et transformation des données
def load_transform_data(true_data):
    true_data_c=true_data.iloc[0:208, 1:-3]
    true_data_c.columns = range(1, 22)
    true_data_c['Votant']= range(1,209)
    true_data_M = true_data_c.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    true_data_m = true_data_M.melt(id_vars=['Votant'], var_name='Place', value_name='Joueur')
    true_data_p=true_data_m.pivot_table(index='Votant', columns='Joueur', values='Place', aggfunc='first')
    true_data_p["FOX"]=true_data_p["FOX"].fillna(true_data_p["DE'AARON FOX"])
    true_data_p["JJJ"]=true_data_p["JJJ"].fillna(true_data_p["JAREN JACKSON JR"])
    true_data_p["CHET"]=true_data_p["CHET"].fillna(true_data_p["HOLMGREN"])
    true_data_p["CHET"]=true_data_p["CHET"].fillna(true_data_p["HOLGREM"])
    true_data_p=true_data_p.drop(columns=["DE'AARON FOX","JAREN JACKSON JR","HOLMGREN","HOLGREM"])
    true_data_f=true_data_p.fillna(22)
    true_data_f["Editorial_Member"]=False
    true_data_f["FOX"]=true_data_f["FOX"].astype(int)
    true_data_f["JJJ"]=true_data_f["JJJ"].astype(int)
    true_data_f["CHET"]=true_data_f["CHET"].astype(int)
    return true_data_f

def get_stats(player):
    stats_json = playercareerstats.PlayerCareerStats(
            player_id=get_player_id(player),
            per_mode36 = "PerGame",
            )
    stats_data = json.loads(stats_json.get_json())
    relevant_data = stats_data['resultSets']

    # Convertir le JSON en DataFrames
    dfs = json_to_df(relevant_data)
    return dfs

def json_to_df(result_sets):
    result_dfs = {}
    
    # Parcourir les resultSets
    for result_set in result_sets:
        name = result_set['name']
        headers = result_set['headers']
        row_set = result_set['rowSet']
        
        # Ignorer les resultSets vides
        if row_set:
            df = pd.DataFrame(row_set, columns=headers)
            result_dfs[name] = df
    
    return result_dfs

def display_df(player):
    dfs = get_stats(player)
    for name, df in dfs.items():
        st.write(f"{name}:")
        st.table(df)  # Afficher les premières lignes du DataFrame
        st.write("\n")