
import pymongo
from st_pages import hide_pages
import streamlit as st
from app_components import sidebar_nav
from auth import authenticate
st.set_page_config(layout="wide", page_title="ProjectGPT")
import uuid
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi 
from streamlit_js_eval import streamlit_js_eval
from chatbot_utils import check_user_login, gather_feedback, handle_submit, handle_withdrawal, local_css, init_connection, study_approval, update_chat_db, write_data



#-------------------------------------Style Settings------------------------------------------------
local_css("./styles.css")
#------------------------------------------USER Authentication-------------------------------------------
check_user_login()
#------------------------------------------DATABASE CONNECTION-------------------------------------------
# client = init_connection()
# connection_string = st.secrets["mongo"]["uri"]
# if connection_string:
#     client = pymongo.MongoClient(connection_string)
#     db = client['users']
# else:
#     raise ValueError("Invalid MongoDB URI. Please check your Streamlit secrets.")
# # collection_access = 'cycle_3'
# collection_name = "usertests" 
#------------------------------------------PAGE LAYOUT----------------------------------------------------

st.title("Velkommen til InnSpillAI – din AI-læringsassistent")

def login_form():
    """Displays the form for both new and returning users."""
    
    st.subheader("Log In")
    
    # st.caption("Enter your personal details")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    return username, password

if st.session_state['page'] == 'login':
    # print("form for False is_logged_in activated")
    # Display the form for users who are not logged in
    with st.form("test_form"):
        is_new_user = st.session_state.get('user_id') is None
        
        username,password = login_form()  # Show the login form
        
        # Set the submit button text based on the user status
        submit_text = "Log In" 
        
        # Create a button container to manage the form button
        button_container = st.empty()
        
        # Pass button_container along with other parameters to handle_submit
        if button_container.form_submit_button(submit_text):
            handle_submit(is_new_user,username,password)
            # Explicitly set is_logged_in to True after the form is submitted
            
if "chat_nullifier" not in st.session_state:
    st.session_state['chat_nullifier'] = False
# Default to 'terms' page if not set in session state
if st.session_state.get('page', 'terms') == 'terms':
    
    # Show the information after the user logs in
    st.subheader("Informasjon om prosjektet")
    st.write("InnSpill AI er en prototype av en virtuell assistent basert på GPT-teknologi. ProjectGPT skal støtte studenter i læringen av kursene. Ansvarlig person er Prof. Anh Nguyen-Duc, institutt for økonomi og informatikk, Handelshøyskolen, Universitetet i Sørøst-Norge.")
    # Confidentiality and Data Protection
    st.subheader("Konfidensialitet og databeskyttelse")
    lst = [
        "Vi vil kun bruke din informasjon til de formålene som er oppgitt i dette dokumentet", 
        "Alle personopplysninger som samles inn under denne studien, vil bli behandlet konfidensielt og i samsvar med personvernreglene.", 
        "Vi vil iverksette nødvendige tekniske og organisatoriske tiltak for å sikre dine data.", 
        "Dataene lagres sikkert i en sikker database og vil kun være tilgjengelig for forskningsteamet."
    ]
    s = '\n'.join([f"- {item}" for item in lst])
    st.markdown(s)
    # Approval button for continuing the study
    if st.button("Godkjenn og Fortsett"):
        study_approval()
        # Use the exact file name without the .py extension
        st.session_state['notification'] = False
        st.switch_page("pages/Project_Buddy.py")

    if st.button("Klikk for å trekke deg"):
        # Handle the withdrawal process
        handle_withdrawal()
        st.write("Du har trukket deg fra studien. Dine data vil bli slettet.")

else:
    # Show a message or form to prompt the user to log in
    st.info("Vennligst logg inn for å se prosjektinformasjonen.")
    
