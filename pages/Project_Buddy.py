import uuid
import streamlit as st
import os
#from decouple import config
import openai
import streamlit as st
#from streamlit_chat import message
from email.policy import default
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import openai
from datetime import datetime
import pymongo



st.set_page_config(layout = "wide", page_title="StartupGPT")
from auth import log_out


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




# Interactive Tutor Tab

st.title("🏢 Interactive Tutor")
st.markdown("""
    Ask for explanation and examples by inputting a prompt.
""", unsafe_allow_html=True)

with st.form("my_form"):
    jim_line = st.text_area("Write your command here:", "", height=10, key='option')
    submitted = st.form_submit_button("Submit")

if submitted and jim_line:  

    if st.session_state['chat_activated'] == False:
        print("form submitted")
        username = st.session_state['username']
        result = collection.find({"username":username})
        chat_id = str(uuid.uuid4()) 
        st.session_state['chat_id'] = chat_id
        print(" new chat_id assigned to session_state")
        new_message = {
            "role": "user",
            "message": jim_line,
            "timestamp": datetime.now().isoformat(),
        }
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": jim_line}
            ]
        )
        assistant_response = response.choices[0].message.content
        bot_response = {
            "role": "bot",
            "message": assistant_response,
            "timestamp": datetime.now().isoformat(),
        }
        collection.insert_one({
            "chat_id":chat_id,
            "username":username,
            "title": " ".join(new_message['message'].split()[:10]),
            "created_at":datetime.now(),
            "messages": [
                new_message,
                bot_response,
            ]

        })
        print("new insertion in chats collection !")
        st.session_state['chat_activated'] = True
        
    else:
        
        chat_id = st.session_state['chat_id']
        new_prompt = {
            "role": "user",
            "message": jim_line,
            "timestamp": datetime.now().isoformat()
        }
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": jim_line}
            ]
        )
        assistant_response = response.choices[0].message.content
        bot_response = {
            "role": "bot",
            "message": assistant_response,
            "timestamp": datetime.now().isoformat(),
        }
        

        # Use update_one to append new messages to the messages array
        collection.update_one(
            {
                "chat_id": chat_id,      # Match the chat_id
                "username": username     # Match the username
            },
            {
                "$push": {
                    "messages": {
                        "$each": [new_prompt, bot_response]  # Add both prompt and response
                    }
                }
            }
        )
        print("appended")
            
    
            

if st.session_state['chat_activated'] == True: # this checks whether the id_status is True, when shouldnt it work?
    chat_id = st.session_state['chat_id']
    chat_history = collection.find_one({"username":username,"chat_id":chat_id})
    if chat_history == None:
        st.write("waiting for the chat ... ")
    else:

        print("the chat_history owrked")
        
        for message in chat_history['messages']:
            if message['role'] == 'user':
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
                        <h4 style="color: #4CAF50; margin-bottom: 5px;">💬 User Input:</h4>
                        <p style="font-size: 16px; color: #333;">{message['message']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            elif message['role'] == 'bot':
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-bottom: 10px; background-color: #f1f1ff;">
                    <h4 style="color: #2196F3; margin-bottom: 5px;">🤖 BOT Response:</h4>
                    <p style="font-size: 16px; color: #555;">{message['message']}</p>
                </div>
                """, unsafe_allow_html=True)
else:
    print("the chat_history didnt owrk")
