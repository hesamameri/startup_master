from datetime import date
from datetime import datetime
import pymongo
import streamlit as st
import extra_streamlit_components as stx
import time
from streamlit_extras.switch_page_button import switch_page
st.set_page_config(layout="wide")
from auth import log_out 
import openai
import time
import pymongo
from datetime import date
import time

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
#################### do not need this everywhere
#if "chat_activated" not in st.session_state:
#    st.session_state['chat_activated'] = False
#
#if 'chat_id_status' not in st.session_state:
#    chats = list(collection.find({"username": username}))  # Convert cursor to list for reuse
#    count = len(chats)  # Count documents directly from the list
#    print("A works and id_status will be assigned true")
#    st.session_state['chat_id_status'] = True
#
#    if chats and count > 0:
#        print("B works")
#        grouped_chats = {}
#        for chat in chats:
#            # Check the structure of `created_at` and handle accordingly
#            if isinstance(chat['created_at'], datetime):
#                created_at = chat['created_at'].date()
#            else:
#                created_at = datetime.fromtimestamp(
#                    int(chat['created_at']['$date']['$numberLong']) / 1000
#                ).date()
#            grouped_chats.setdefault(created_at, []).append(chat)
#
#        with st.sidebar.expander("Chat History", expanded=False):
#            for date, chats_for_date in sorted(grouped_chats.items(), key=lambda item: item[0], reverse=True):
#                st.markdown(f"### {date.strftime('%A, %B %d, %Y')}")  # Display date header
#                for chat in chats_for_date:
#                    if st.button(chat['title']):
#                        st.session_state['chat_id'] = chat['chat_id']
#                        st.session_state['chat_activated'] = True
#                        st.switch_page('pages/Project_Buddy.py')
#    else:
#        print("C works")
#        st.sidebar.page_link('pages/Project_Buddy.py', label='Chat History')
#else:
#    if st.session_state['chat_id_status'] == True:
#        print("D works")
#        chats = list(collection.find({"username": username}))  # Convert cursor to list for reuse
#        count = len(chats)
#        if chats and count > 0:
#            print("F works")
#            grouped_chats = {}
#            for chat in chats:
#                # Check the structure of `created_at` and handle accordingly
#                if isinstance(chat['created_at'], datetime):
#                    created_at = chat['created_at'].date()
#                else:
#                    created_at = datetime.fromtimestamp(
#                        int(chat['created_at']['$date']['$numberLong']) / 1000
#                    ).date()
#                grouped_chats.setdefault(created_at, []).append(chat)
#
#            with st.sidebar.expander("Chat History", expanded=False):
#                for date, chats_for_date in sorted(grouped_chats.items(), key=lambda item: item[0], reverse=True):
#                    st.markdown(f"### {date.strftime('%A, %B %d, %Y')}")  # Display date header
#                    for chat in chats_for_date:
#                        if st.button(chat['title']):
#                            st.session_state['chat_id'] = chat['chat_id']
#                            st.session_state['chat_activated'] = True
#                            st.switch_page('pages/Project_Buddy.py')
#        else:
#            print("H works")
#            st.sidebar.page_link('pages/Project_Buddy.py', label='Chat History')
#chat_button = st.sidebar.button("Start New Chat") 
#if chat_button:
#    st.session_state['chat_activated'] = False
#    st.switch_page('pages/Project_Buddy.py')
###################

st.sidebar.page_link('pages/Project_Buddy.py', label='InnSpill Compis')
st.sidebar.page_link('pages/Getting_Feedback.py', label='Getting Feedback')
st.sidebar.page_link('pages/Your_Progress.py', label='Your Progress')

st.sidebar.page_link('pages/Keeping_Track.py', label='Keeping Track')
st.sidebar.page_link('pages/Meeting_Room.py', label='Meeting Room')
if st.sidebar.button("Log Out"):
    log_out()  # Call the log_out function when the button is clicked



# Header and date display
st.header("Summary of your team progress")
today = date.today()
st.write("Here we summarize your learning progress up to ", today)




user_collection = db['usertests']
class_collection = db['class']
project_collection = db['projects']
exercise_def_collection = db['Exercise_def']
exercises_collection = db['exercises']

def calculate_assignment_progress(username):
    """
    Calculate the assignment progress percentage for a user.
    """
    print(username)
    # Retrieve user data to get their class
    user_data = user_collection.find_one({"username": username})
    if not user_data:
        st.error("User not found!")
        return 0

    
    if "class" not in user_data:
        class_name = "USN25_PRO1000_Bo"
    else:
        class_name = user_data["class"]
    # Filter Exercise_def records for the user's class
    exercise_def_records = exercise_def_collection.find({"class": class_name})
    
    total_exercises = 0
    for record in exercise_def_records:
        exercises = record.get("exercises", [])
        if isinstance(exercises, list):
            total_exercises += len(exercises)  # Each entry in the list represents one exercise

    if total_exercises == 0:
        st.error("No exercises defined for this class!")
        return 0

    # Count completed exercises for the user in the exercises collection
    completed_exercises = exercises_collection.count_documents({"user_id": username})
    
    # Calculate progress percentage
    progress = int((completed_exercises / total_exercises) * 100)
    
    return progress

    

# Ensure username exists in session state
if "username" not in st.session_state:
    st.error("Username not found in session state!")
else:
    username = st.session_state["username"]

    with st.spinner("Loading progress bars..."):
        # Simulate delay for demonstration
        time.sleep(2)

        # Calculate assignment progress
        assignment_progress = calculate_assignment_progress(username)
        
        # Display progress bars
        my_assignment = st.progress(
            assignment_progress, 
            text=f"You have completed {assignment_progress:.2f}% of your exercises in this course"
        )
        my_milestones = st.progress(50, text="You should have completed 1/2 obligatory assignments in this course")
        my_meeting = st.progress(15, text="You should have completed 1/7 obligatory meetings or surveys with InnSpill")
        my_group_presentation = st.progress(0, text="You have completed 0/2 obligatory group presentations in this course")