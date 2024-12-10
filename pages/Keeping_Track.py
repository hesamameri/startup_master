import openai
import pymongo
import streamlit as st
import extra_streamlit_components as stx
import time
from streamlit_extras.switch_page_button import switch_page
from datetime import date, datetime, timedelta
from pymongo import MongoClient
from auth import log_out


st.set_page_config(layout="wide") 
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



######################################### MAIN PAGE

# set token for launching the retrieval button
# set token for loading the latest progress form
# make the retrieval button activate a function that does the retrieval or creates a form record for the user in 
# in the database. database name -> project_def ( has each form itemgroup  / checkbox or multi selectbox)
# i want to either create :
#{"title": "sth","order_num": 1 "items": [{"name":"sth","type" : "selectbox",  value: ['']},{"name":"sth", "type":"checkbox","value": false},..] }  
# or retrieve the items of the form accordingly


# UI and Database connection setup
# Database setup (example only; replace with your actual credentials and collection names)
# Database setup
st.header("Reflecting on your learning progress")
st.write("To keep track of your learning progress, we need to collect some information from you.")
st.write("Please complete the form seriously as it might impact the feedback you will receive.")

connection_string = st.secrets['mongo']['uri']
client = pymongo.MongoClient(connection_string)
db = client['users']
destination_collection = db["projects"]
user_id = st.session_state['user_id']

# Initialize session state for retrieved data
if "retrieved_data" not in st.session_state:
    st.session_state["retrieved_data"] = {}

# Button to retrieve form data
if st.button("Retrieve Latest Form Data"):
    # Fetch the latest document for the specific user
    user_data = destination_collection.find_one({"user_id": st.session_state['user_id']})
    if user_data:
        # Update session state with retrieved data
        st.session_state["retrieved_data"] = user_data
        st.success("Form data retrieved successfully!")
    else:
        st.warning("No data found for the user.")

# Display the form
with st.form("this"):
    # Populate form fields with retrieved data or default values
    st.write("Team Formation")
    team_stage = st.selectbox(
        "Team Stage",
        options=['Found a team', 'Understand'],
        index=['Found a team', 'Understand'].index(
            st.session_state["retrieved_data"].get("TeamStage", "Found a team")
        )
    )
    st.write("Project Planning")
    project_spec = st.checkbox("Project Specification", value=st.session_state["retrieved_data"].get("ProjectSpec", False))
    project_req = st.checkbox("Project Requirements", value=st.session_state["retrieved_data"].get("ProjectReq", False))
    communication = st.checkbox("Communication", value=st.session_state["retrieved_data"].get("Communication", False))
    project_management = st.checkbox("Project Management", value=st.session_state["retrieved_data"].get("ProjectManagement", False))
    ide_setup = st.checkbox("IDE Setup", value=st.session_state["retrieved_data"].get("IDESetup", False))
    collaboration = st.checkbox("Collaboration", value=st.session_state["retrieved_data"].get("Collaboration", False))
    learning_experience = st.checkbox("Learning Experience", value=st.session_state["retrieved_data"].get("LearningExperience", False))
    wbs = st.selectbox(
        "WBS",
        options=['CreateAV', 'ValidateAV'],
        index=['CreateAV', 'ValidateAV'].index(
            st.session_state["retrieved_data"].get("WBS", "CreateAV")
        )
    )
    st.write("Risk Assessment")
    risk_score = st.checkbox("Risk Score", value=st.session_state["retrieved_data"].get("RiskScore", False))
    risk_count = st.checkbox("Risk Count", value=st.session_state["retrieved_data"].get("RiskCount", False))
    role = st.checkbox("Role", value=st.session_state["retrieved_data"].get("Role", False))
    define = st.checkbox("Define", value=st.session_state["retrieved_data"].get("Define", False))

    submitted_form = st.form_submit_button("Submit Form")
    # Submit button to insert or update values in the database
    # Submit button to insert or update values in the database
    if submitted_form:
        # Collect the values into a dictionary for database insertion or update
        user_inputs = {
            "user_id": user_id,  # Add user identifier
            "TeamStage": team_stage,
            "ProjectSpec": project_spec,
            "ProjectReq": project_req,
            "Communication": communication,
            "ProjectManagement": project_management,
            "IDESetup": ide_setup,
            "Collaboration": collaboration,
            "LearningExperience": learning_experience,
            "WBS": wbs,
            "RiskScore": risk_score,
            "RiskCount": risk_count,
            "Role": role,
            "Define": define,
        }
        print(st.session_state)
        # Check if user_id exists in the collection
        existing_record = destination_collection.find_one({"user_id": user_id})

        if existing_record:
            print("record exists")
            # Update the existing record
            destination_collection.update_one(
                {"user_id": user_id},  # Match by user_id
                {"$set": user_inputs}  # Update fields with new values
            )
            st.success("Form updated successfully!")
        else:
            # Insert a new record if user_id doesn't exist
            print("record doesnt exist")
            result = destination_collection.insert_one(user_inputs)
            st.success(f"Form submitted successfully! Document ID: {result.inserted_id}")

        # Clear session state items
        if "retrieved_data" in st.session_state:
            print("cache deleted")
            del st.session_state["retrieved_data"]




















    

