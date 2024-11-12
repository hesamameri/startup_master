import streamlit as st
import extra_streamlit_components as stx
import time
from streamlit_extras.switch_page_button import switch_page
st.set_page_config(layout="wide")
from auth import log_out 

st.sidebar.page_link('pages/Project_Buddy.py', label='Project Buddy')
st.sidebar.page_link('pages/Your_Progress.py', label='Your Progress')
st.sidebar.page_link('pages/Customer_Meeting.py', label='Customer Meeting')
if st.sidebar.button("Log Out"):
    log_out()  # Call the log_out function when the button is clicked


st.header("All tasks")
st.write("Here we summarize your learning progress!")
