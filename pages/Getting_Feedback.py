from datetime import datetime
import time
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
from pymongo.errors import PyMongoError
from auth import log_out
st.set_page_config(layout = "wide", page_title="InnSpillAI")




openai.api_key = st.secrets["api"]["key"]
connection_string = st.secrets['mongo']['uri']
client = pymongo.MongoClient(connection_string)
db = client['users']
collection = db['chats']

# session state checks
if 'page' not in st.session_state:  # Check if 'page' key exists
    st.session_state['page'] = 'login'
    st.switch_page("Chatbot.py")
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


st.sidebar.page_link('pages/Project_Buddy.py', label='InnSpill Compis')
st.sidebar.page_link('pages/Getting_Feedback.py', label='Getting Feedback')
st.sidebar.page_link('pages/Your_Progress.py', label='Your Progress')
st.sidebar.page_link('pages/Keeping_Track.py', label='Keeping Track')
st.sidebar.page_link('pages/Meeting_Room.py', label='Meeting Room')

if st.sidebar.button("Log Out"):
    log_out()  # Call the log_out function when the button is clicked 


# Initialize variables
cathy_line = ''
jim_line = ''
starting_line = ''

def get_response(jim_line):
    return "dummy"

database_name = "users"
collection_name = "Exercise_def"

def add_exercise_item(item, collection_name='exercises'):
    client = pymongo.MongoClient(connection_string)
    db = client[database_name]
    collection = db[collection_name]
    
    # Query to find an existing record with the same username and exercise title
    query = {"user_id": item["user_id"], "title": item["title"]}
    existing_item = collection.find_one(query)
    
    if existing_item:
        # If the item exists, check and increment "attempts"
        current_attempts = existing_item.get("attempts", 0)
        if current_attempts >= 3:
            message = "Update blocked. Maximum attempts reached."
            return False,message
           
        
        # Update response, timestamp, and increment attempts
        collection.update_one(
            query,
            {
                "$set": {
                    "response": item["response"],
                    "timestamp": item["timestamp"]
                },
                "$inc": {"attempts": 1}  # Increment attempts by 1
            }
        )
        message = f"Item updated successfully. Attempt {current_attempts + 1}/3."
        
        return True,message
        
    else:
        # If the item doesn't exist, insert it with "attempts" set to 1

        item["attempts"] = 1
        collection.insert_one(item)
        message = "Insertion successful. Attempt 1/3."
        st.success(message)
        return True,message

# MongoDB connection string
connection_string = st.secrets['mongo']['uri']
client = pymongo.MongoClient(connection_string)
db = client[database_name]
collection = db[collection_name]
exercise_collection = db['exercises']

users_collection = db['usertests']
current_user = st.session_state['username']
class_current_user = users_collection.find_one({"username":current_user})
class_name = class_current_user['class']
# add the code for users class retrieval and use it in the query for modules
print(current_user)
print(class_name)
##############
def check_submission_feedback(task_name):
    collection = db['exercises']
    username = st.session_state['username']
    # Query to find an existing record with the same username and exercise title
    query = {"user_id": username, "title": task_name}
    exercise_selected = collection.find_one(query)
    if exercise_selected:
        feedback_status = exercise_selected['feedback_sent']
        
        if feedback_status:
            
            return exercise_selected['feedback']
        else:
        
            return None
    else:
        return False
#############


try:
    print(class_name)
    query = {"class":class_name}
    modules = collection.find(query)  # Fetch all documents
    print(modules)
    module_names = [record["module_name"] for record in modules if "module_name" in record]
    print(module_names)
    # Check if module_names is non-empty
    if module_names:
        tabs = st.tabs(module_names)
        selected_task = None

        for i, module_name in enumerate(module_names):
            tab = tabs[i]
            with tab:
                module_record = collection.find_one({"module_name": module_name})

                if module_record:
                    module_description = module_record.get('module_description', 'No description available.')
                    st.write(f"**Module Description**: {module_description}")
                    if 'submission' in st.session_state:
                        del st.session_state['submission']
                    tasks = module_record.get('exercises', [])
                    tasks_count = len(tasks)
                    cols = st.columns(tasks_count)
                    selected_task = None

                    for idx, task in enumerate(tasks):
                        col = cols[idx]
                        with col:
                            unique_key = f"{i}_{module_name}_{idx}"
                            if st.button(task['title'], key=unique_key, use_container_width=True):
                                selected_task = task
                                st.session_state['selected_task'] = selected_task
                                st.session_state['ai_instruction'] = task['ai_instruction']

                    if selected_task:
                        st.markdown(f"**Description**  \n {selected_task['exercise_description']}", unsafe_allow_html=True)
                        
                        
                    
                    
                    
                    
                   



                    with st.expander("Submit your exercise here"):
                        with st.form(f"my_form_{i}"):
                            email_feedback = st.text_input("Email to receive feedback", "12345678@std.usn")
                            response = st.text_area("Write your exercise here", "", height=200)
                            submitted = st.form_submit_button("Submit")

                        if submitted:
                            item = st.session_state['selected_task']
                            item['user_id'] = st.session_state['username']
                            item['class'] = module_record['class']
                            item['email_feedback'] = email_feedback
                            item['response'] = response
                            item['feedback'] = None
                            item['feedback_grade'] = 1
                            item['feedback_sent'] = False
                            item['timestamp'] = datetime.now()
                            # submission_status,message = 
                            st.session_state['submission'] = add_exercise_item(item)
                    # Simulating submission
                    if 'submission' in st.session_state:
                        success_message = st.session_state['submission'][1]
                        message_placeholder = st.empty()  # Create an empty placeholder
                        message_placeholder.info(success_message)  # Show success message
                    else:
                        st.info("Please submit your exercise")

                    st.markdown(
                            f"""
                            <h2> Feedback Section </h2>
                            <aside style="background-color: #f1f1f1; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">
                                <strong>Notification:</strong> Choose the exercise to see the corresponding feedback.
                            </aside>
                            """, 
                            unsafe_allow_html=True
                        )
                    if 'selected_task' in st.session_state:
                        
                        set_status = check_submission_feedback(st.session_state['selected_task']['title'])
                        
                        if set_status is not None and set_status:
                            st.markdown(
                                f"""
                                <div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                                    <h2 style="font-weight: bold; font-size: 24px; text-align: center; color: black;">Feedback</h2>
                                    <p style="font-size: 18px; color: black; line-height: 1.6; padding: 10px 0;">
                                        {set_status}
                                    </p>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                            
##################################################
                else:
                    st.info("This module has no available data. Please check back later.")
    else:
        st.warning("No modules yet. Wait for further instruction.")

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

#####################################################