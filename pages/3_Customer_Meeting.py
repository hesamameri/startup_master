import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
import app_components as components 

st.set_page_config(layout = "wide", page_title="Customer Meeting")
col1, col2 = st.columns([1, 3])
with col1:
        st.header("Reidar Hellegurd")
        st.image("https://www.nih.no/om/ansatte/reidars/reidar_safvenbom_250x250.jpg",width=300)
with col2:
        st.markdown("The meetings with customers are scheduled. Today you will talk to your Customer Reidar Hellegurd")
        st.markdown("The objective of the meeting is to clarify the customer's need. Read the project description and prepare your questions. An example of questions can be - What is the prefered color scheme for the home page? How the cover photo should look like? ")
        st.markdown ("""
                Ask for explanation and examples by input a prompt.
            """, unsafe_allow_html=False)
        with st.form("my_form"):
                jim_line = st.text_area("Write you question here","", height=70)
                submitted = st.form_submit_button("Submit")

