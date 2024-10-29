import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
import app_components as components 

st.set_page_config(layout = "wide", page_title="Customer Meeting")

st.markdown("The meetings with customers are scheduled.")

