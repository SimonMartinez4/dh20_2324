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

# Import functions
from functions import json_to_df
from functions import vote_graph
from functions import get_player_id
from functions import load_transform_data
from functions import get_stats
from functions import json_to_df
from functions import display_df

st.cache_data

def run():

    # Parameters selectboxes
    player_options=["BAM",
    "BANCHERO",
    "BARNES",
    "BOOKER",
    "BRIDGES",
    "BROWN",
    "BRUNSON",
    "BUTLER",
    "CADE",
    "CASON WALLACE",
    "CHET",
    "CURRY",
    "DAVIS",
    "DEMAR",
    "DONCIC",
    "DURANT",
    "EDWARDS",
    "EMBIID",
    "FOX",
    "GEORGE",
    "GIANNIS",
    "GOBERT",
    "GREEN",
    "HALIBURTON",
    "HARDEN",
    "HERRO",
    "JDUB",
    "JJJ",
    "JOKIC",
    "JRUE",
    "KAWHI",
    "KYRIE",
    "LAMELO",
    "LEBRON",
    "LILLARD",
    "LUGUENTZ DORT",
    "MARKKANEN",
    "MAXEY",
    "MITCHELL",
    "MORANT",
    "MURRAY",
    "PORZINGIS",
    "RANDLE",
    "SABONIS",
    "SENGUN",
    "SGA",
    "SIAKAM",
    "TATUM",
    "TOWNS",
    "VICTOR",
    "WESTBROOK",
    "WHITE",
    "YOUNG",
    "ZION"]

    player = st.selectbox('Joueur', player_options)
    player_vote = st.button('Obtenir les votes')

    if player_vote :
        player_id = get_player_id(player)
        vote_graph(player)
        display_df(player)