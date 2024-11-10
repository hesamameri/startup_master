
import pymongo
import streamlit as st
st.set_page_config(layout="wide", page_title="ProjectGPT")
import uuid
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi 
from streamlit_js_eval import streamlit_js_eval
from chatbot_utils import check_user_login, gather_feedback, handle_submit, handle_withdrawal, local_css, init_connection, update_chat_db, write_data



#-------------------------------------Style Settings------------------------------------------------
local_css("./styles.css")
#------------------------------------------USER Authentication-------------------------------------------
check_user_login()
#------------------------------------------DATABASE CONNECTION-------------------------------------------
# client = init_connection()
connection_string = st.secrets["mongo"]["uri"]
if connection_string:
    client = pymongo.MongoClient(connection_string)
    print("successful connection")
    db = client.usertests
    backup_db = client.usertests_backup
else:
    raise ValueError("Invalid MongoDB URI. Please check your Streamlit secrets.")
collection_access = 'cycle_3'
#------------------------------------------PAGE LAYOUT----------------------------------------------------

st.title("Welcome to ProjectGPT")

def display_form():
    # """Displays the form for both new and returning users."""
    
    
    st.subheader("Log In")
    #st.caption("Personal details")
    st.session_state['username'] = st.text_input("Enter your username", value=st.session_state.get('username', ''), placeholder="Group12_2025")
    st.session_state['password'] = st.text_input("Enter your password", value=st.session_state.get('password', ''), placeholder="mypassword", )
    
# Check if the user is already logged in (use session state)
if not st.session_state.get('is_logged_in', False):
    # Display the form for users who are not logged in
    with st.form("test_form"):
        is_new_user = st.session_state.get('user_id') is None

        display_form()  # Show the login form

        # Set the submit button text based on the user status
        submit_text = "Log In" if is_new_user else "Click to update form information"
        
        # Create a button container to manage the form button
        button_container = st.empty()

        # Pass button_container along with other parameters to handle_submit
        if button_container.form_submit_button(submit_text):
            handle_submit(is_new_user, submit_text, db, backup_db, button_container, collection_access)
            # Explicitly set is_logged_in to True after the form is submitted
            st.session_state['is_logged_in'] = True
            
else:
    # If already logged in, show an info message instead of the form
    st.info("You are already logged in.")
    


if st.session_state.get('is_logged_in', False):
    # Show the information after the user logs in
    st.subheader("Information about the project")
    st.write("ProjectGPT is a prototype of a virtual assistant built on GPT technology. ProjectGPT will support students to learn from the courses")

    st.subheader("Who is responsible for the research project?")
    st.write("Department of Economic and Informatikk, Business School, University of South Eastern Norway")
    
    st.subheader("Voluntary Participation")
    st.write("Your participation in this study is entirely voluntary. You have the right to withdraw at any time without any negative consequences. If you wish to withdraw all the data obtained concerning you for this study is deleted immediately. You will not be able to recover your data after withdrawing. To withdraw from the study click the button below:")
    
    withdraw_button_container = st.empty()

    with st.container():
        withdraw_button_container = st.empty()  # Empty container for dynamic button
        button_container = st.empty()  # Another container for form buttons

        # Call the handle_withdrawal function with the database connections
        handle_withdrawal(withdraw_button_container, button_container, client, db, backup_db)

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
else:
    # Show a message or form to prompt the user to log in
    st.info("Please log in to view the project information.")

