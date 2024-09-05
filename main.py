# -*- coding: utf-8 -*-
"""

@author: Simon Martinez
"""

# Import packages
import requests
from PIL import Image
from io import BytesIO
import streamlit as st
import votes
import stats
import glossary
import test_db

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
pages = ["**Votes 2023-24**","**Stats DH20 2023-24**","**Glossaire**", "**Test DB**"]
page = st.sidebar.radio("Menu", pages)
if page == pages[0]:
    votes.run()
elif page == pages[1]:
    stats.run()
elif page == pages[2]:
    glossary.run()
elif page == page[3]:
    test_db.run()

st.sidebar.markdown("---")

url="https://yt3.googleusercontent.com/ytc/AIdro_lbykwSVSSVHZm49kHKRTm19CiW80MpDwcfLUhccmwaIFM=s900-c-k-c0x00ffffff-no-rj"
response = requests.get(url)
response.raise_for_status()
image = Image.open(BytesIO(response.content))
st.sidebar.image(image, use_column_width=True)