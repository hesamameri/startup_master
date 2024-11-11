import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
st.set_page_config(layout = "wide", page_title="Customer Meeting")
from streamlit_extras.switch_page_button import switch_page
import app_components as components
from auth import log_out 

st.sidebar.page_link('pages/Project_Buddy.py', label='Project Buddy')
st.sidebar.page_link('pages/Your_Progress.py', label='Your Progress')
st.sidebar.page_link('pages/Customer_Meeting.py', label='Customer Meeting')
if st.sidebar.button("Log Out"):
    log_out()  # Call the log_out function when the button is clicked


st.markdown("The meetings with customers are scheduled.")

