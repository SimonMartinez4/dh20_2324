## Import packages

import streamlit as st

# NBA api endpoints
from nba_api.stats.endpoints import playerestimatedmetrics
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashplayerstats

#Dataviz
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

    fig.patch.set_alpha(0.0)  # Rendre le fond de la figure transparent
    ax.set_facecolor('none')  # Rendre le fond des axes transparent

    # Créer un violon plot en excluant les membres de la rédaction
    sns.violinplot(x='Editorial_Member', y=joueur, data=df_non_editorial, inner='quartile', color='skyblue', ax=ax, label="Communauté DH")

    # Ajouter un swarm plot pour les membres de la rédaction
    #sns.swarmplot(x='Editorial_Member', y=joueur, data=df_editorial, color='blue', ax=ax, label='Rédaction DH')

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
    #handles.append(plt.Line2D([0], [0], color='lightgray', lw=4))

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
    pd.set_option('future.no_silent_downcasting', True)
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
    true_data_f=true_data_p.fillna(22).infer_objects(copy=False)
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

def advanced(season_type):
    try :   
        player_json = leaguedashplayerstats.LeagueDashPlayerStats(
                measure_type_detailed_defense = "Advanced",
                per_mode_detailed = "PerGame",
                season = "2023-24",
                season_type_all_star = season_type
                )
        player_data = json.loads(player_json.get_json())
        relevant_data = player_data['resultSets'][0]
        headers = relevant_data['headers']
        rows = relevant_data['rowSet']
        data = pd.DataFrame(rows)
        data.columns = headers
        a_data = data[['PLAYER_ID','PLAYER_NAME','GP','MIN','TS_PCT','USG_PCT']]
    except Exception as e :
        a_data=None
    return a_data

def scoring(season_type):
    try:
        player_json = leaguedashplayerstats.LeagueDashPlayerStats(
                measure_type_detailed_defense = "Scoring",
                per_mode_detailed = "PerGame",
                season = "2023-24",
                season_type_all_star = season_type
                )
        player_data = json.loads(player_json.get_json())
        relevant_data = player_data['resultSets'][0]
        headers = relevant_data['headers']
        rows = relevant_data['rowSet']
        data = pd.DataFrame(rows)
        data.columns = headers
        s_data=data[['PLAYER_ID','PCT_AST_FGM']]
    except Exception as e:
        s_data=None
    return s_data

def stats(season_type):
    try:
        a_data=advanced(season_type)
        s_data=scoring(season_type)
        data = pd.merge(a_data,s_data, on='PLAYER_ID', how='left')
    except Exception as e :
        data=None
    return data

def graph(player,season_type):
    player_id=get_player_id(player)
    data=stats(season_type)
    if player_id in data['PLAYER_ID'].values :
        # Ajouter les sliders pour filtrer les données
        min_minutes = st.slider("Minutes Jouées Minimum", min_value=0, max_value=int(data['MIN'].max()), value=20)
        min_games = st.slider("Matchs Joués Minimum", min_value=0, max_value=int(data['GP'].max()), value=0)
        min_ast_pct = st.slider("Pourcentage de Tirs Assistés Maximum", min_value=0.0, max_value=100.0, value=50.0)

        # Filtrer les données selon les valeurs sélectionnées par les sliders
        filtered_data = data[
            (data['MIN'] >= min_minutes) &
            (data['GP'] >= min_games) &
            (data['PCT_AST_FGM'] <= min_ast_pct / 100)
        ]

        if player_id in data['PLAYER_ID'].values:
            data_f = filtered_data[filtered_data['PLAYER_ID'] != player_id].reset_index(drop=True)
            data_p = filtered_data[filtered_data['PLAYER_ID'] == player_id].reset_index(drop=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                            x=data_f['USG_PCT'],
                            y=data_f['TS_PCT'],
                            hovertext= data_f[['PLAYER_NAME', 'TS_PCT', 'USG_PCT', 'PCT_AST_FGM']].apply(
                                lambda row: f'{row["PLAYER_NAME"]} => True Shooting :{round(row["TS_PCT"]*100,2)} % - Usage Rate : {round(row["USG_PCT"]*100,2)} % - Assisted Field Goals : {round(row["PCT_AST_FGM"]*100,2)} %',
                                axis=1
                                ),
                            hoverinfo='text',
                            mode='markers',
                            marker=dict(
                                        size=5,
                                        color='red'
                                        )
                            #text='PLAYER_NAME',
            ))

            fig.add_trace(go.Scatter(
                            x=data_p['USG_PCT'],
                            y=data_p['TS_PCT'],
                            text=data_p['PLAYER_NAME'],
                            textposition='top left',
                            textfont=dict(
                                        size=18,
                                        color='black'
                                        ),
                            hovertext= data_p[['PLAYER_NAME', 'TS_PCT', 'USG_PCT', 'PCT_AST_FGM']].apply(
                                lambda row: f'{row["PLAYER_NAME"]} => True Shooting :{round(row["TS_PCT"]*100,2)} % - Usage Rate : {round(row["USG_PCT"]*100,2)} % - Assisted Field Goals : {round(row["PCT_AST_FGM"]*100,2)} %',
                                axis=1
                                ),
                            hoverinfo='text',
                            mode='markers+text',
                            marker=dict(
                                        size=10,
                                        color='black'
                                        )
            ))



            # Mise à jour des axes et des grilles
            fig.update_xaxes(
                title="Usage Percentage (USG%)",
                showgrid=True,  # Afficher la grille
                gridcolor='black',  # Couleur de la grille en noir
                titlefont=dict(color='black'),  # Titre de l'axe en noir
                tickfont=dict(color='black')  # Étiquettes de l'axe en noir
            )

            fig.update_yaxes(
                title="True Shooting Percentage (TS%)",
                showgrid=True,  # Afficher la grille
                gridcolor='black',  # Couleur de la grille en noir
                titlefont=dict(color='black'),  # Titre de l'axe en noir
                tickfont=dict(color='black')  # Étiquettes de l'axe en noir
            )


            fig.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',)

            return st.plotly_chart(fig, use_container_width=True)
    else :
        return st.write(f"{player} didn't play any {season_type} game in 2023-24")