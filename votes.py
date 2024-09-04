## Import packages

import streamlit as st

# Other packages
import pandas as pd

# Import xlsx data
true_data=pd.read_excel('./src/data_dh20.xlsx', sheet_name='Réponses individuelles')
ids=pd.read_excel('./src/dh20_ids.xlsx',sheet_name='Feuil1')

# Import functions
from functions import vote_graph

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

    player = st.selectbox('Joueur', player_options)
    #st.session_state.player = player

    # Mise à jour et affichage du graphique des votes dès que le joueur est sélectionné
    if player:
        vote_graph(player)
