import streamlit as st
import toml
import pymongo
import bcrypt
# def load_user_credentials():
#     try:
#         secrets = toml.load(".streamlit/secrets.toml")  # Assuming the secrets.toml file is in the same directory
#         return secrets.get("users", {})
#     except Exception as e:
#         st.error(f"Failed to load credentials from secrets.toml: {e}")
#         return {}



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
    st.switch_page('Chatbot.py')