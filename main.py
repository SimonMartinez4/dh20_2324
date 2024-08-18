# -*- coding: utf-8 -*-
"""

@author: Simon Martinez
"""

# Import packages
import streamlit as st
import votes

def basketball_theme():
    st.set_page_config(
        page_title="DH20 2023-24",
        page_icon=":basketball:",
        layout="centered",
    )

basketball_theme()

# Function to load or change style
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load local CSS file
local_css("style.css")

st.sidebar.markdown("DH20")
pages = ["**Votes 2023-24**"]
page = st.sidebar.radio("Menu", pages)
if page == pages[0]:
    votes.run()

st.sidebar.markdown("---")