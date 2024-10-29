import streamlit as st
from st_pages import add_indentation, hide_pages,show_pages_from_config
import extra_streamlit_components as stx
import time
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(layout="wide") 

st.header("All tasks")
st.write("Here we summarize your learning progress!")
