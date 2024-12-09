from datetime import datetime
import pymongo
import streamlit as st
from openai import OpenAI
import os
#from decouple import config
import openai
import streamlit as st
#from streamlit_chat import message
from email.policy import default
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from auth import log_out
st.set_page_config(layout = "wide", page_title="StartupGPT")
#import app_components as components 
#import chatbot_utils as cu

# client = OpenAI(api_key=st.secrets["OPENAI_KEY"])
# DB connection
openai.api_key = st.secrets["api"]["key"]
connection_string = st.secrets['mongo']['uri']
client = pymongo.MongoClient(connection_string)
db = client['users']
collection = db['chats']

# session state checks
if 'page' not in st.session_state:  # Check if 'page' key exists
    st.session_state['page'] = 'login'
# pop up welcome message
if 'notification' not in st.session_state:
    st.session_state['notification'] = True
elif st.session_state['notification'] == False:
    username = st.session_state["username"]
    st.markdown(
        f"""
        <div style="
            padding: 20px; 
            background-color: #e0f7fa; 
            color: #006064; 
            font-size: 24px; 
            font-weight: bold;
            border-radius: 10px;
            text-align: center;
            ">
            Welcome to PRO1000, {username}!
        
        </div>
        """,
        unsafe_allow_html=True
    )
    st.session_state['notification'] = True
   
username = st.session_state["username"]

if "chat_activated" not in st.session_state:
    st.session_state['chat_activated'] = False


if 'chat_id_status' not in st.session_state:
    chats = list(collection.find({"username": username}))  # Convert cursor to list for reuse
    count = len(chats)  # Count documents directly from the list
    print("A works and id_status will be assigned true")
    st.session_state['chat_id_status'] = True

    if chats and count > 0:
        print("B works")

        grouped_chats = {}
        for chat in chats:
            # Check the structure of `created_at` and handle accordingly
            if isinstance(chat['created_at'], datetime):
                created_at = chat['created_at'].date()
            else:
                created_at = datetime.fromtimestamp(
                    int(chat['created_at']['$date']['$numberLong']) / 1000
                ).date()

            grouped_chats.setdefault(created_at, []).append(chat)

        with st.sidebar.expander("Chat History", expanded=False):
            for date, chats_for_date in sorted(grouped_chats.items(), key=lambda item: item[0], reverse=True):
                st.markdown(f"### {date.strftime('%A, %B %d, %Y')}")  # Display date header
                for chat in chats_for_date:
                    if st.button(chat['title']):
                        st.session_state['chat_id'] = chat['chat_id']
                        st.session_state['chat_activated'] = True
                        st.switch_page('pages/Project_Buddy.py')

    else:
        print("C works")
        st.sidebar.page_link('pages/Project_Buddy.py', label='Chat History')

else:
    if st.session_state['chat_id_status'] == True:
        print("D works")
        chats = list(collection.find({"username": username}))  # Convert cursor to list for reuse
        count = len(chats)

        if chats and count > 0:
            print("F works")

            grouped_chats = {}
            for chat in chats:
                # Check the structure of `created_at` and handle accordingly
                if isinstance(chat['created_at'], datetime):
                    created_at = chat['created_at'].date()
                else:
                    created_at = datetime.fromtimestamp(
                        int(chat['created_at']['$date']['$numberLong']) / 1000
                    ).date()

                grouped_chats.setdefault(created_at, []).append(chat)

            with st.sidebar.expander("Chat History", expanded=False):
                for date, chats_for_date in sorted(grouped_chats.items(), key=lambda item: item[0], reverse=True):
                    st.markdown(f"### {date.strftime('%A, %B %d, %Y')}")  # Display date header
                    for chat in chats_for_date:
                        if st.button(chat['title']):
                            st.session_state['chat_id'] = chat['chat_id']
                            st.session_state['chat_activated'] = True
                            st.switch_page('pages/Project_Buddy.py')

        else:
            print("H works")
            st.sidebar.page_link('pages/Project_Buddy.py', label='Chat History')

  



chat_button = st.sidebar.button("Start New Chat") 
if chat_button:
    st.session_state['chat_activated'] = False
    st.switch_page('pages/Project_Buddy.py')
st.sidebar.page_link('pages/Getting_Feedback.py', label='Getting Feedback')
st.sidebar.page_link('pages/Your_Progress.py', label='Your Progress')
st.sidebar.page_link('pages/Keeping_Track.py', label='Keeping Track')
st.sidebar.page_link('pages/Meeting_Room.py', label='Meeting Room')

if st.sidebar.button("Log Out"):
    log_out()  # Call the log_out function when the button is clicked 
cathy_line =''
jim_line = ''
starting_line = ''
def get_response(jim_line):
    output =  "dummy"
    return output                                                                                                                                                                                                             
database_name = "users"
collection_name = "Exercise_def"



connection_string = st.secrets['mongo']['uri']
client = pymongo.MongoClient(connection_string)
db = client[database_name]
collection = db[collection_name]
modules = collection.find()

# Extract module names from the documents
module_names = [key for record in modules for key in record.keys() if isinstance(record[key], dict)]

# Create tabs based on the number of modules
tabs = st.tabs(module_names)

# Display each module in the loop
for i, tab_name in enumerate(module_names):
    tab = tabs[i]
    with tab:
        # Query the module data from the collection
        module_record = collection.find_one({tab_name: {'$exists': True}})
        if module_record:
            module_data = module_record[tab_name]
            image_url = module_data['image']
            st.image(image_url, caption=tab_name, width=400)  # Display the image
            
            # Get tasks from the module data
            tasks = module_data['exercises']
            tasks_count = len(tasks)  # Count the number of tasks
            
            # Create columns based on the number of tasks
            cols = st.columns(tasks_count)
            for idx, task in enumerate(tasks):
                col = cols[idx]
                with col:
                    st.button(task['title'], key=task['key'], use_container_width=True)
            with st.expander("Submit your exercise here"):
                with st.form(f"my_form{i}"):
                    jim_email = st.text_input("Email to receive feedback", "12345678@std.usn")
                    jim_line = st.text_area("Write your exercise here", "", height=200)
                    submitted = st.form_submit_button("Submit")







