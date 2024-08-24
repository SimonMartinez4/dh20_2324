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

# Import functions
from functions import json_to_df
from functions import vote_graph
from functions import get_player_id
from functions import load_transform_data
from functions import get_stats
from functions import json_to_df
from functions import display_df
from functions import advanced
from functions import scoring
from functions import stats
from functions import graph

st.cache_data

def run():
    # Initialisation des variables de session si elles n'existent pas
    if 'player' not in st.session_state:
        st.session_state.player = None
    if 'season_type' not in st.session_state:
        st.session_state.season_type = None

    st.header("Votes DH20 2023-24")
    # Choix du joueur
    player_options = ["BAM", "BANCHERO", "BARNES", "BOOKER", "BRIDGES", "BROWN", "BRUNSON", "BUTLER", "CADE",
                      "CASON WALLACE", "CHET", "CURRY", "DAVIS", "DEMAR", "DONCIC", "DURANT", "EDWARDS", "EMBIID",
                      "FOX", "GEORGE", "GIANNIS", "GOBERT", "GREEN", "HALIBURTON", "HARDEN", "HERRO", "JDUB", "JJJ",
                      "JOKIC", "JRUE", "KAWHI", "KYRIE", "LAMELO", "LEBRON", "LILLARD", "LUGUENTZ DORT", "MARKKANEN",
                      "MAXEY", "MITCHELL", "MORANT", "MURRAY", "PORZINGIS", "RANDLE", "SABONIS", "SENGUN", "SGA",
                      "SIAKAM", "TATUM", "TOWNS", "VICTOR", "WESTBROOK", "WHITE", "YOUNG", "ZION"]

    player = st.selectbox('Joueur', player_options, index=player_options.index(st.session_state.player) if st.session_state.player else 0)
    st.session_state.player = player

    # Mise à jour et affichage du graphique des votes dès que le joueur est sélectionné
    if player:
        vote_graph(player)

    st.header("Efficacité")
    # Choix du type de saison
    season_type = st.selectbox('Saison Régulière / Playoffs', ["Regular Season", "Playoffs"], index=["Regular Season", "Playoffs"].index(st.session_state.season_type) if st.session_state.season_type else 0)
    st.session_state.season_type = season_type

    # Mise à jour et affichage du graphique du True Shooting %
    if player and season_type:
        try:
            graph(player, season_type)

        except TypeError:
            st.error("Les données du joueur ne sont pas disponibles pour cette saison ou ce type de saison.")
