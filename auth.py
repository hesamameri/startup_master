import streamlit as st
import toml
import pymongo
import bcrypt



def authenticate(username, password, database_name='users', collection_name='usertests'):
    # Access the specified database and collection
    connection_string = st.secrets['mongo']['uri']
    client = pymongo.MongoClient(connection_string)
    db = client[database_name]
    collection = db[collection_name]
    
    # Find the user document by username
    user = collection.find_one({'username': username})
    
    # Check if user exists and if the password matches
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        print("Login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False

def log_out():
    st.session_state['user_id'] = None
    st.session_state['page'] = 'login'
    if 'chat_id_status' in st.session_state:
        del st.session_state["chat_id_status"]
    if 'chat_activated' in st.session_state:
        del st.session_state["chat_activated"]
    if 'chat_history' in st.session_state:
        del st.session_state['chat_history']
    st.switch_page('Chatbot.py')