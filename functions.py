## Import packages

import streamlit as st

# NBA api endpoints
from nba_api.stats.endpoints import playerestimatedmetrics
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.endpoints import leaguehustlestatsplayer
from nba_api.stats.endpoints import playerdashptreb
from nba_api.stats.endpoints import leaguedashptdefend
from nba_api.stats.endpoints import leaguedashptstats


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
    true_data_M = true_data_c.map(lambda x: x.upper() if isinstance(x, str) else x)
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

def advanced(season_type):
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
        a_data = data[['PLAYER_ID','PLAYER_NAME','GP','MIN','TS_PCT','USG_PCT','AST_RATIO','PIE',]]
        return a_data

def scoring(season_type):
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
        return s_data

def shotdef(season_type):
        player_json = leaguedashptdefend.LeagueDashPtDefend(
                defense_category = "Overall",
                league_id = "00",
                per_mode_simple = "PerGame",
                season = "2023-24",
                season_type_all_star = season_type,
                )
        player_data = json.loads(player_json.get_json())
        relevant_data = player_data['resultSets'][0]
        headers = relevant_data['headers']
        rows = relevant_data['rowSet']
        data = pd.DataFrame(rows)
        data.columns = headers
        d_data=data[['CLOSE_DEF_PERSON_ID','PCT_PLUSMINUS']]
        d_data=d_data.rename(columns={'CLOSE_DEF_PERSON_ID':"PLAYER_ID"})
        return d_data

def reb(season_type):
        player_json = leaguedashptstats.LeagueDashPtStats(
                player_or_team = "Player",
                pt_measure_type = "Rebounding",
                per_mode_simple = "PerGame",
                season = "2023-24",
                season_type_all_star = season_type,
                )
        player_data = json.loads(player_json.get_json())
        relevant_data = player_data['resultSets'][0]
        headers = relevant_data['headers']
        rows = relevant_data['rowSet']
        data = pd.DataFrame(rows)
        data.columns = headers
        r_data=data[['PLAYER_ID','REB_CHANCE_PCT_ADJ']]
        return r_data

def keystats(season_type):
    dh20_p=ids.loc[ids["dh20"]==1,["player_id","po"]]
    dh20_p=dh20_p.rename(columns={"player_id":"PLAYER_ID"})
    adv=advanced(season_type)
    scor=scoring(season_type)
    sdef=shotdef(season_type)
    areb=reb(season_type)
    keystats1=pd.merge(dh20_p,adv, on='PLAYER_ID', how='inner')
    keystats2=pd.merge(keystats1,scor, on="PLAYER_ID", how='inner')
    keystats3=pd.merge(keystats2,sdef, on="PLAYER_ID", how='inner')
    keystats=pd.merge(keystats3,areb, on="PLAYER_ID", how='inner')
    keystats=keystats.rename(columns={"TS_PCT":"True Shooting %",
                                      "USG_PCT":"Usage %",
                                      "AST_RATIO":"Assists Ratio",
                                      "PCT_AST_FGM":"Assisted FG %",
                                      "PCT_PLUSMINUS":"Defensive Diff %",
                                      "REB_CHANCE_PCT_ADJ":"Adjusted Rebound Chance %"})
    cols=["True Shooting %","Assists Ratio","Adjusted Rebound Chance %","PIE"]
    df_rank = keystats[cols].rank(axis=0, method='min', ascending=False)
    df_rank = df_rank.astype(int)
    df_rankd = keystats["Defensive Diff %"].rank(axis=0, method='min', ascending=True)
    df_rankd = pd.DataFrame(df_rankd)
    df_rankd=df_rankd.astype(int)
    df_rank.columns = [f'Rank {col}' for col in cols]
    df_rankd.columns = ["Rank Defensive Diff %"]
    keystats = pd.concat([keystats, df_rank, df_rankd], axis=1)
    return keystats

def polar(player, season_type):
    
    player_id=get_player_id(player)
    df=keystats(season_type)
    cols=["Rank True Shooting %","Rank Assists Ratio","Rank Adjusted Rebound Chance %","Rank Defensive Diff %"]
    cols_name=["PLAYER_NAME","Rank True Shooting %","Rank Assists Ratio","Rank Adjusted Rebound Chance %","Rank Defensive Diff %"]
    df_player=df.loc[df["PLAYER_ID"]==player_id,cols_name].reset_index()

    if player_id in df['PLAYER_ID'].values :    
        r_values = df_player.loc[0, cols].values
        text_labels = [f"{col}: {value}" for col, value in zip(cols, r_values)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=df_player.loc[0,cols].values,
            theta=cols,
            fill='toself',
            name=df_player.loc[0,'PLAYER_NAME'],
            line=dict(color='royalblue', width=1),
            text=text_labels,
            hoverinfo='text'
            ))
        

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    gridcolor="black",
                    visible=True,
                    range=[20, 1],
                    tickvals=[20,15,10,5,1],
                    tickfont=dict(color="black")
                ),
                angularaxis=dict(
                    gridcolor="black",
                    tickfont=dict(color="black")
                )
            ),
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        return st.plotly_chart(fig, use_container_width=True)
    else :
        return st.write(f"{player} didn't play any {season_type} game in 2023-24")

def pie(player, season_type):
    df=keystats(season_type)
    player_id=get_player_id(player)
    df_player=df.loc[df["PLAYER_ID"]==player_id,['PLAYER_NAME','PIE','Rank PIE']].reset_index(drop=True)
    pie=round(df_player.loc[0,"PIE"]*100,2)
    rankpie=round(df_player.loc[0,"Rank PIE"],0)
    return pie, rankpie


def eff_graph(player,season_type):
    player_id=get_player_id(player)
    data=keystats(season_type)
    if player_id in data['PLAYER_ID'].values :
        data_f=data[data['PLAYER_ID'] != player_id].reset_index(drop=True)
        data_p=data[data['PLAYER_ID'] == player_id].reset_index(drop=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=data_f['Usage %'],
                        y=data_f['True Shooting %'],
                        hovertext= data_f[['PLAYER_NAME', 'True Shooting %', 'Usage %', 'Assisted FG %']].apply(
                            lambda row: f'{row["PLAYER_NAME"]} => True Shooting :{round(row["True Shooting %"]*100,2)} % - Usage % : {round(row["Usage %"]*100,2)} % - Assisted Field Goals : {round(row["Assisted FG %"]*100,2)} %',
                            axis=1
                            ),
                        hoverinfo='text',
                        mode='markers'
                        #text='PLAYER_NAME',
        ))

        fig.add_trace(go.Scatter(
                        x=data_p['Usage %'],
                        y=data_p['True Shooting %'],
                        text=data_p['PLAYER_NAME'],
                        textposition='bottom right',
                        textfont=dict(
                                    size=18,
                                    color="red"
                                    ),
                        hovertext= data_p[['PLAYER_NAME', 'True Shooting %', 'Usage %', 'Assisted FG %']].apply(
                            lambda row: f'{row["PLAYER_NAME"]} => True Shooting :{round(row["True Shooting %"]*100,2)} % - Usage % : {round(row["Usage %"]*100,2)} % - Assisted Field Goals : {round(row["Assisted FG %"]*100,2)} %',
                            axis=1
                            ),
                        hoverinfo='text',
                        mode='markers+text',
                        marker=dict(
                                    size=10,
                                    )
        ))

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

        # Affichage des noms des joueurs sur les points du scatterplot
        fig.update_traces(
            #title='Scatterplot of TS% vs USG% for Players',
        )

        fig.update_layout(
            template='plotly_dark',
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',)

        return st.plotly_chart(fig, use_container_width=True)
    else :
        return st.write(f"{player} didn't play any {season_type} game in 2023-24")

def ast_graph(player,season_type):
    player_id=get_player_id(player)
    data=keystats(season_type)
    if player_id in data['PLAYER_ID'].values :
        data_f=data[data['PLAYER_ID'] != player_id].reset_index(drop=True)
        data_p=data[data['PLAYER_ID'] == player_id].reset_index(drop=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=data_f['Usage %'],
                        y=data_f['Assists Ratio'],
                        hovertext= data_f[['PLAYER_NAME', 'Assists Ratio', 'Usage %']].apply(
                            lambda row: f'{row["PLAYER_NAME"]} => Assists Ratio :{row["Assists Ratio"]} % - Usage % : {round(row["Usage %"]*100,2)} %',
                            axis=1
                            ),
                        hoverinfo='text',
                        mode='markers'
                        #text='PLAYER_NAME',
        ))

        fig.add_trace(go.Scatter(
                        x=data_p['Usage %'],
                        y=data_p['Assists Ratio'],
                        text=data_p['PLAYER_NAME'],
                        textposition='bottom right',
                        textfont=dict(
                                    size=18,
                                    color="red"
                                    ),
                        hovertext= data_p[['PLAYER_NAME', 'Assists Ratio', 'Usage %']].apply(
                            lambda row:f'{row["PLAYER_NAME"]} => Assists Ratio :{row["Assists Ratio"]} % - Usage % : {round(row["Usage %"]*100,2)} %',
                            axis=1
                            ),
                        hoverinfo='text',
                        mode='markers+text',
                        marker=dict(
                                    size=10,
                                    )
        ))



        fig.update_xaxes(
            title="Usage Percentage (USG%)",
            showgrid=True,  # Afficher la grille
            gridcolor='black',  # Couleur de la grille en noir
            titlefont=dict(color='black'),  # Titre de l'axe en noir
            tickfont=dict(color='black')  # Étiquettes de l'axe en noir
            )

        fig.update_yaxes(
            title="Assists Ratio",
            showgrid=True,  # Afficher la grille
            gridcolor='black',  # Couleur de la grille en noir
            titlefont=dict(color='black'),  # Titre de l'axe en noir
            tickfont=dict(color='black')  # Étiquettes de l'axe en noir
            )

        # Affichage des noms des joueurs sur les points du scatterplot
        fig.update_traces(
            #title='Scatterplot of TS% vs USG% for Players',
        )

        fig.update_layout(
            template='plotly_dark',
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',)

        return st.plotly_chart(fig, use_container_width=True)
    else :
        return st.write(f"{player} didn't play any {season_type} game in 2023-24")

def ddiff_graph(player, season_type):
    
    df=keystats(season_type)
    df=df.sort_values(by='Defensive Diff %', ascending=False)
    player_id=get_player_id(player)
    
    if player_id in df['PLAYER_ID'].values :

        player_to_annotate = df.loc[df["PLAYER_ID"]==player_id,"PLAYER_NAME"].reset_index(drop=True)[0]

        fig = go.Figure()
    
        fig.add_trace(go.Bar(
            x=df["Defensive Diff %"],
            y=df["PLAYER_NAME"],
            orientation = 'h',
            text=[player if player == player_to_annotate else '' for player in df["PLAYER_NAME"]],
            textfont=dict(size=20, color="black"),
            textposition="outside",
            hovertext= df[['PLAYER_NAME', 'Defensive Diff %']].apply(
                            lambda row: f'{row["PLAYER_NAME"]} => Defensive Diff % : {round(row["Defensive Diff %"]*100,2)} %',
                            axis=1
                            ),
            hoverinfo='text'
        )
        )

        fig.update_layout(
            template='plotly_dark',
            xaxis_title='Défensive Diff %',
            yaxis=dict(
                showticklabels=False
            ),
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',        
        )

        fig.update_xaxes(
            showgrid=True,  # Afficher la grille
            gridcolor='black',  # Couleur de la grille en noir
            titlefont=dict(color='black'),  # Titre de l'axe en noir
            tickfont=dict(color='black')  # Étiquettes de l'axe en noir
            )
        
        return st.plotly_chart(fig, use_container_width=True)
    
    else:
        return st.write(f"{player} didn't play any playoffs game in 2023-24")
    
def reb_graph(player, season_type):
    df=keystats(season_type)
    df=df.sort_values(by='Adjusted Rebound Chance %', ascending=True)
    player_id=get_player_id(player)
    
    if player_id in df['PLAYER_ID'].values:
        
        player_to_annotate = df.loc[df["PLAYER_ID"]==player_id,"PLAYER_NAME"].reset_index(drop=True)[0]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df["PLAYER_NAME"],
            y=df["Adjusted Rebound Chance %"],
            orientation = 'v',
            text=[player if player == player_to_annotate else '' for player in df["PLAYER_NAME"]],
            hovertext= df[['PLAYER_NAME', 'Adjusted Rebound Chance %']].apply(
                            lambda row: f'{row["PLAYER_NAME"]} => Adjusted Rebound Chance % : {round(row["Adjusted Rebound Chance %"]*100,2)} %',
                            axis=1
                            ),
            hoverinfo='text'
        )
        )

        fig.update_layout(
            xaxis_title='Adjusted Rebound Chance %',
            xaxis=dict(
                showticklabels=False
            ),
            yaxis=dict(
                showticklabels=True
            ),
            template='plotly_dark',
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        fig.update_yaxes(
            showgrid=True,  # Afficher la grille
            gridcolor='black',  # Couleur de la grille en noir
            titlefont=dict(color='black'),  # Titre de l'axe en noir
            tickfont=dict(color='black')  # Étiquettes de l'axe en noir
            )
        
        fig.update_xaxes(
            showgrid=False,  # Afficher la grille
            gridcolor='black',  # Couleur de la grille en noir
            titlefont=dict(color='black'),  # Titre de l'axe en noir
            tickfont=dict(color='black')  # Étiquettes de l'axe en noir
            )

        return st.plotly_chart(fig, use_container_width=True)
    else :
        return st.write(f"{player} didn't play any playoffs game in 2023-24")

def base(season_type):
    player_json = leaguedashplayerstats.LeagueDashPlayerStats(
            per_mode_detailed = "PerGame",
            season = "2023-24",
            season_type_all_star = season_type,
            )
    player_data = json.loads(player_json.get_json())
    relevant_data = player_data['resultSets'][0]
    headers = relevant_data['headers']
    rows = relevant_data['rowSet']
    data = pd.DataFrame(rows)
    data.columns = headers
    data=data.iloc[:,:32]
    return data

def hustle(season_type):
    player_json = leaguehustlestatsplayer.LeagueHustleStatsPlayer(
            per_mode_time = "PerGame",
            season = "2023-24",
            season_type_all_star = season_type,
            )
    player_data = json.loads(player_json.get_json())
    relevant_data = player_data['resultSets'][0]
    headers = relevant_data['headers']
    rows = relevant_data['rowSet']
    data = pd.DataFrame(rows)
    data.columns = headers
    return data

def allstats(season_type):
    dh20_p=ids.loc[ids["dh20"]==1,["player_id","po"]]
    dh20_p=dh20_p.rename(columns={"player_id":"PLAYER_ID"})
    bs=base(season_type)
    hsl=hustle(season_type)
    stats=pd.merge(dh20_p,bs, on='PLAYER_ID', how='inner')
    stats=pd.merge(stats,hsl, on="PLAYER_ID", how='inner')
    stats.drop(['NICKNAME',
                'TEAM_ID_x',
                'TEAM_ABBREVIATION_x',
                'AGE_x',
                'PLAYER_NAME_y',
                'MIN_y',
                'TEAM_ID_y',
                'TEAM_ABBREVIATION_y',
                'AGE_y',
                'G'], axis=1, inplace = True)
    stats=stats.rename(columns={'PLAYER_NAME_x':'PLAYER_NAME','MIN_x':'MIN'})
    return stats

def custom_graph(player,season_type,y):
    
    player_id=get_player_id(player)
    data=allstats(season_type)
    
    if player_id in data['PLAYER_ID'].values :
        data_f=data[data['PLAYER_ID'] != player_id].reset_index(drop=True)
        data_p=data[data['PLAYER_ID'] == player_id].reset_index(drop=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=data_f['MIN'],
                        y=data_f[y],
                        hovertext= data_f[['PLAYER_NAME', 'MIN', y]].apply(
                            lambda row: f'{row["PLAYER_NAME"]} => {y} :{row[y]} - Min : {row["MIN"]}',
                            axis=1
                            ),
                        hoverinfo='text',
                        mode='markers'
                        #text='PLAYER_NAME',
        ))

        fig.add_trace(go.Scatter(
                        x=data_p['MIN'],
                        y=data_p[y],
                        text=data_p['PLAYER_NAME'],
                        textposition='bottom right',
                        textfont=dict(
                                    size=18,
                                    color='red'
                                    ),
                        hovertext= data_p[['PLAYER_NAME', 'MIN', y]].apply(
                            lambda row: f'{row["PLAYER_NAME"]} => {y} :{row[y]} - Min : {row["MIN"]}',
                            axis=1
                            ),
                        hoverinfo='text',
                        mode='markers+text',
                        marker=dict(
                                    size=10,
                                    )
        ))



        fig.update_xaxes(
            title="Avg Minutes"
            )

        fig.update_yaxes(
            title=y
               )
        
        fig.update_yaxes(
            showgrid=True,  # Afficher la grille
            gridcolor='black',  # Couleur de la grille en noir
            titlefont=dict(color='black'),  # Titre de l'axe en noir
            tickfont=dict(color='black')  # Étiquettes de l'axe en noir
            )
        
        fig.update_xaxes(
            showgrid=True,  # Afficher la grille
            gridcolor='black',  # Couleur de la grille en noir
            titlefont=dict(color='black'),  # Titre de l'axe en noir
            tickfont=dict(color='black')  # Étiquettes de l'axe en noir
            )

        # Affichage des noms des joueurs sur les points du scatterplot
        fig.update_traces(
            #title='Scatterplot of TS% vs USG% for Players',
        )

        fig.update_layout(
            showlegend=False,
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )

        return st.plotly_chart(fig, use_container_width=True)
    
    else :
        return st.write(f"{player} didn't play any {season_type} game in 2023-24")

def get_url_img(player):
    player_id = get_player_id(player)
    player_url=f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
    return player_url