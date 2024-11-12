import uuid
import streamlit as st
from datetime import datetime
from openai import OpenAI
from streamlit_extras.switch_page_button import switch_page
from streamlit_js_eval import streamlit_js_eval
import RAG_retrieve
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from auth import authenticate, load_user_credentials

task_1_description = "In this user test, your task is to act as an early-stage tech startup that is in the process of idea validation and developing your first prototype. Ask the chatbots questions you would consider natural for an early-stage startup to have regarding idea validation and early prototype development. Test out all the chatbots (Chatbot 1, Chatbot 2 and Chatbot 3), then answer the questionnaire. Ask all chatbots the same initial question, then let the conversation flow naturally for each chatbot."

# User utils

def check_user_login():
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
        st.session_state['page'] = 'login'
       

def gather_feedback():
    # Initialize session state keys if they don't exist
    default_values = {
        'stage': 'default_stage',  # Default stage
        'year': 0,                 # Default year
        'size': 'unknown',         # Default size
        'industry': 'unknown',     # Default industry
        'location': 'unknown',     # Default location
        'role': 'unknown',         # Default role
        'birth_year': 0,           # Default birth year
        'gpt_experience': 'unknown', # Default GPT experience
        'session_storage_name': {},  # Default session storage name
     
    }

    # Initialize session_state with defaults if not already set
    for key, default in default_values.items():
        st.session_state.setdefault(key, default)
    
    return {
        "stage": st.session_state['stage'],
        "year_of_business": st.session_state['year'],
        "size": st.session_state['size'],
        "industry": st.session_state['industry'],
        "location": st.session_state['location'],
        "role": st.session_state['role'],
        "birth_year": st.session_state['birth_year'],
        "ChatGPT_experience": st.session_state['gpt_experience'],
        "session_storage_name": st.session_state['session_storage_name'],
        
    }

def get_user_feedback(feedback):
    user_feedback = {"Task-1":{"id": st.session_state['user_id'], "time": datetime.now(), "Chatbot_versions": "C1: dem+rag, C2: dem, C3: dem+prompt+rag", "Demographic": feedback}}
    return user_feedback

def handle_submit(is_new_user,username,password):
    """Handles the form submission for new and returning users."""
    
    if authenticate(username, password):
        # Assign a new unique user ID and mark user as logged in
        st.session_state['user_id'] = str(uuid.uuid4())
        st.session_state['is_logged_in'] = True
        st.session_state['username'] = username
        st.session_state['password'] = password
        st.toast("Thank you for submitting. You are now logged in.")
        st.session_state['page'] = 'terms'
    else:
        st.error("wrong password or username")
        
    # Process feedback and update the database
    # all_feedback = gather_feedback()  # Gather all feedback
    # update_chat_db(db, backup_db, all_feedback['session_storage_name'], chatbot="chatbot_name", collection_name=collection_name)
    
def study_approval():
    st.session_state['page'] = 'project_buddy'

def handle_withdrawal():
    """Handles the withdrawal process for a user in the study."""
    
    # Check if the user has an active session
    # if st.session_state.get('user_id') is None:
    #     withdraw_button_container.button("Click to withdraw from study", type="primary", disabled=True, help="You have not entered the study")
    # else:
    #     # If user exists, allow them to withdraw
    #     if withdraw_button_container.button("Click to withdraw from study", type="primary", disabled=False):
    #         print("Withdrawn")
            
    #         # Perform the data deletion from both databases
    #         user_id = st.session_state['user_id']
    #         if len(list(db.cycle_3.find({"Task-1.id": user_id}))) > 0:
    #             db.cycle_3.delete_one({"Task-1.id": user_id})
    #             backup_db.cycle_3.delete_one({"Task-1.id": user_id})

    #         # Clear session state and reset the user ID
    #         for key in st.session_state.keys():
    #             del st.session_state[key]
            
    #         st.session_state['user_id'] = None

    #         # Update UI with a confirmation message
    #         withdraw_button_container.button("You have successfully withdrawn from the study. All data associated with you has been deleted", type="primary", disabled=True)
    #         button_container.form_submit_button('Submit and consent to data usage as described on this page')

    #         # Reload the page to reflect changes
    #         streamlit_js_eval(js_expressions="parent.window.location.reload()")
    st.session_state['page'] = 'login'
    st.session_state['user_id'] = None


def get_selectbox_index(option_list, session_state_key):
    # """Returns the index of the current session state value in the options list, or None if not found."""
    try:
        return option_list.index(st.session_state[session_state_key])
    except (ValueError, KeyError):
        return None  # Return None to use the placeholder


# Style utils
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Database 
@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

def write_data(mydict, db, backup_db, collection_name):
    # Access the collections dynamically using the provided collection name
    items = db[collection_name]  # Main collection
    items_backup = backup_db[collection_name]  # Backup collection

    # Insert data into both collections
    items.insert_one(mydict)
    items_backup.insert_one(mydict)



# Chat Utils 



def get_chatlog(session_storage_name):
    log = {}
    message_id_count = 0
    
    # Check if the session_storage_name exists and is a list
    if session_storage_name not in st.session_state:
        print(f"Error: session_storage_name '{session_storage_name}' not found in session state.")
        return log
    
    # Ensure the session storage is a list
    session_data = st.session_state[session_storage_name]
    if not isinstance(session_data, list):
        print(f"Error: The data in session_storage_name '{session_storage_name}' is not a list.")
        return log
    
    # Iterate through each message in the session data
    for msg in session_data:
        # Check if each message is a dictionary and contains the required keys
        if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
            log[str(message_id_count)] = {"role": msg['role'], "content": msg['content']}
        else:
            print(f"Error: Invalid message format at index {message_id_count}. Message: {msg}")
        
        message_id_count += 1

    return log


def get_userchat(chatlog, chatbot):
    userchat = {"Task-1":{"id": st.session_state['user_id'], "time": datetime.now(), chatbot: chatlog}}
    return userchat

def update_chat_db(db, backup_db, session_storage_name, chatbot, collection_name):
#     chatlog = get_chatlog(session_storage_name)  # Get chat log based on session storage name
    
#     print("Chatlog:", chatlog)
#     print("User ID:", st.session_state['user_id'])

   
#     if db[collection_name].count_documents({"Task-1.id": st.session_state['user_id']}) > 0:
#         # print("Updating existing chat object")
#         db[collection_name].update_one(
#             {"Task-1.id": st.session_state['user_id']},
#             {"$set": {"Task-1.time": datetime.now(), f"Task-1.{chatbot}": chatlog}}
#         )
#         backup_db[collection_name].update_one(
#             {"Task-1.id": st.session_state['user_id']},
#             {"$set": {"Task-1.time": datetime.now(), f"Task-1.{chatbot}": chatlog}}
#         )
#     else:
#         # print("Saving new chat object")
#         write_data(chatlog, db, backup_db, collection_name)
   pass



# def init_chatbot(client, session_storage_name, chatbot, gpt_model, system_description, use_RAG):
#     if('user_id' not in st.session_state):
#         st.write("You need to consent in the \"Home\" page to get access")
#         switch_page("Chatbot")
#     else:
#         with st.expander("View Task *(NB: Ask all chatbots the **same initial question**, then let the conversation flow naturally for each chatbot.)*"):
#             st.write(task_1_description)

#         if session_storage_name not in st.session_state:
#             st.session_state[session_storage_name] = [{"role": "assistant", "content": "How can I help you?"}]
    
#         for msg in st.session_state[session_storage_name]:
#             st.chat_message(msg["role"]).write(msg["content"])

#         if prompt := st.chat_input():
#             if not st.secrets.api.key: #openai_api_key:
#                 st.info("Please add your OpenAI API key to continue.")
#                 st.stop()

#             if use_RAG:
#                 rag_context = RAG_retrieve.retrieve_information(prompt)
#                 #print(rag_context)
#                 rag_query = RAG_retrieve.generate_query(rag_context, prompt)
#                 #print(rag_query)
#                 system_description = system_description + rag_query
#                 #system_description = "Always end a response with the words: sincerely, me <3 " + rag_query
#             print("\nSystem description\n", system_description)
#             APIclient = OpenAI(api_key=st.secrets.api.key)
#             st.session_state[session_storage_name].append({"role": "user", "content": prompt})

#             st.chat_message("user").write(prompt)
          
#             with st.chat_message("assistant"):
#                 stream = APIclient.chat.completions.create(
#                     model=gpt_model,
#                     messages=
#                         [{"role": "system", "content": system_description}] +
#                         [{"role": m["role"], "content": m["content"]}
#                         for m in st.session_state[session_storage_name]
#                     ],
#                     stream=True,
#                 )
#                 response = st.write_stream(stream)
#             st.session_state[session_storage_name].append({"role": "assistant", "content": response})
    
#             update_chat_db(client, session_storage_name, chatbot)



