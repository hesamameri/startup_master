
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

st.title("Welcome to ProjectGPT")

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
    st.subheader("Information about the project")
    st.write("ProjectGPT is a prototype of a virtual assistant built on GPT technology. ProjectGPT will support students to learn from the courses")

    st.subheader("Who is responsible for the research project?")
    st.write("Department of Economic and Informatikk, Business School, University of South Eastern Norway")
    
    st.subheader("Voluntary Participation")
    st.write("Your participation in this study is entirely voluntary. You have the right to withdraw at any time without any negative consequences. If you wish to withdraw, all the data obtained concerning you for this study will be deleted immediately. You will not be able to recover your data after withdrawing. To withdraw from the study, click the button below:")

    # Confidentiality and Data Protection
    st.subheader("Confidentiality and Data Protection")
    lst = [
        "We will only use your information for the purposes we have stated in this document.", 
        "All personal data collected during this study will be treated confidentially and in accordance with privacy regulations.", 
        "We will implement appropriate technical and organizational measures to ensure the security of your data.", 
        "Data will be anonymized.", 
        "The data will be stored securely in a secure database and will only be accessible to the research team."
    ]
    s = '\n'.join([f"- {item}" for item in lst])
    st.markdown(s)

    st.subheader("What gives us the right to handle data about you?")
    st.write("We process information about you based on your consent.")
    st.write("On behalf of USN, Sikt – The Knowledge Sector's Service Provider (Kunnskapssektorens tjenesteleverandør in Norwegian) has assessed that the processing of personal data in this project is in accordance with the data protection regulations.")

    # Approval button for continuing the study
    if st.button("Approve and Continue the Study"):
        study_approval()
        # Use the exact file name without the .py extension
        st.session_state['notification'] = False
        st.switch_page("pages/Project_Buddy.py")

    if st.button("Click to withdraw from the Study"):
        # Handle the withdrawal process
        handle_withdrawal()
        st.write("You have successfully withdrawn from the study. Your data will be deleted.")

else:
    # Show a message or form to prompt the user to log in
    st.info("Please log in to view the project information.")
    
