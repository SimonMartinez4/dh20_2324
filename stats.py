## Import packages

import streamlit as st

# Other packages
import pandas as pd
import matplotlib.image as mpimg
import requests
from PIL import Image
from io import BytesIO

# Pandas config
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Import xlsx data
true_data=pd.read_excel('./src/data_dh20.xlsx', sheet_name='Réponses individuelles')
ids=pd.read_excel('./src/dh20_ids.xlsx',sheet_name='Feuil1')

# Import DH logo

img = mpimg.imread('./src/logo-dunkhebdo.jpg')

# Import functions
from functions import polar
from functions import pie
from functions import eff_graph
from functions import ast_graph
from functions import ddiff_graph
from functions import reb_graph
from functions import custom_graph
from functions import get_url_img

def run():
    # Initialisation des variables de session si elles n'existent pas
    if 'player' not in st.session_state:
        st.session_state.player = None
    if 'season_type' not in st.session_state:
        st.session_state.season_type = None
    if 'stat_choice' not in st.session_state:
        st.session_state.stat_choice = None

    st.header("Stats DH20 2023-24")

    # Choix du joueur
    player_options = ["BOOKER", "BROWN", "BRUNSON", "BUTLER",
                      "CURRY", "DAVIS", "DONCIC", "DURANT", "EDWARDS", "EMBIID",
                      "GIANNIS", "HALIBURTON",
                      "JOKIC", "KAWHI", "KYRIE", "LEBRON",
                      "MITCHELL", "SGA",
                      "TATUM", "VICTOR"]

    player = st.selectbox('Joueur', player_options, index=player_options.index(st.session_state.player) if st.session_state.player else 0)
    season_type = st.selectbox('Saison Régulière / Playoffs', ["Regular Season", "Playoffs"], index=["Regular Season", "Playoffs"].index(st.session_state.season_type) if st.session_state.season_type else 0)

    st.write("")

    if player and season_type :

        try:
            piescore, rankpie = pie(player,season_type)
            col1, col2 = st.columns(2)
            with col1:
                url=get_url_img(player)
                response = requests.get(url)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                st.image(image, use_column_width=True)
                st.write("")
                
            with col2:
                st.metric(label= "Player Impact Estimate", value=piescore)
                st.metric(label= "PIE Rank", value=rankpie)
            
            polar(player, season_type)
            
            st.header("Efficacité")
            eff_graph(player,season_type)
            st.header("Ratio de passes décisives")
            ast_graph(player,season_type)
            st.header("Impact défensif sur l'efficacité de son adversaire")
            ddiff_graph(player,season_type)
            st.header("Efficacité au rebond")
            reb_graph(player,season_type)
            
            st.header("Statistiques de base")
            stat_options=['PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM','FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT',
                          'OREB', 'DREB', 'TOV', 'BLKA', 'PF', 'PFD', 'PLUS_MINUS', 'W_PCT',
                          'CONTESTED_SHOTS', 'CONTESTED_SHOTS_2PT','CONTESTED_SHOTS_3PT', 'DEFLECTIONS', 'CHARGES_DRAWN',
                          'SCREEN_ASSISTS','SCREEN_AST_PTS', 'OFF_LOOSE_BALLS_RECOVERED','DEF_LOOSE_BALLS_RECOVERED',
                          'LOOSE_BALLS_RECOVERED','PCT_LOOSE_BALLS_RECOVERED_OFF', 'PCT_LOOSE_BALLS_RECOVERED_DEF',
                          'OFF_BOXOUTS', 'DEF_BOXOUTS', 'BOX_OUTS', 'BOX_OUT_PLAYER_TEAM_REBS','BOX_OUT_PLAYER_REBS',
                          'PCT_BOX_OUTS_OFF', 'PCT_BOX_OUTS_DEF','PCT_BOX_OUTS_TEAM_REB', 'PCT_BOX_OUTS_REB']
            stat_choice = st.selectbox('Rubrique statistique', stat_options, index=stat_options.index(st.session_state.stat_choice) if st.session_state.stat_choice else 0)
            custom_graph(player,season_type,stat_choice)

        except TypeError:
            st.error(f"{player} n'a pas joué en {season_type} en 2023-2024.")

        