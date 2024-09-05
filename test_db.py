from functions import check_tables, test_db_connection
import os
import streamlit as st

def run():
    st.write("Fichiers dans le répertoire courant :", os.listdir())
    test_db_connection()
    check_tables()