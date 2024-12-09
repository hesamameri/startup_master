import openai
import pymongo
import streamlit as st
import extra_streamlit_components as stx
import time
from streamlit_extras.switch_page_button import switch_page
from datetime import date, datetime, timedelta

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

st.header("Reflecting on your learning progress")
st.write("To keep track on your learning progress, we need to collect some information from you.")
st.write("Please complete the form seriously as it might impact the feedback you will receive.")
st.button("I understand! Let's start")
st.button("Load the latest form to update new progress?")
with st.form("my_form"):
    st.write("To understand your progress, please fill in the following information:")
    
    # Milestone 1 - Project planning
    st.caption("Milestone 1 - Project planning")
    
    # Section 1
    st.write("1. Team formation")
    team_stage = st.selectbox("Stage", options=["No team found", "Found a team", "Agree on way of working", "Storming time", "Performing time"])
    
    # Section 2
    st.write("2. Project specification")
    spec_read = st.checkbox("Read project specification")
    chat_customer = st.checkbox("Chat with the customer")
    understand_need = st.checkbox("Understand what need to do")
    understand_not_do = st.checkbox("Understand what should not do")
    describe_func_req = st.checkbox("Describe the functional requirements")
    describe_non_func_req = st.checkbox("Describe the non-functional requirements")
    
    # Section 3
    st.write("3. Tool and Configuration")
    setup_repo = st.checkbox("Set up a project repository - Github, Dropbox, etc")
    setup_comm_tool = st.checkbox("Set up communication tool - Team, Messenger, Slack, etc")
    setup_pm_board = st.checkbox("Set up a project management board - Trello, Monday, etc")
    setup_dev_env = st.checkbox("Set up a software development environment - Visual Studio, Sublime, etc")
    setup_doc_editor = st.checkbox("Set up a document editor tool - Word 365, Google Doc, etc")
    learn_learnix = st.checkbox("Learn to use LearnIX")
    
    # Section 4
    st.write("4. Scope planning")
    scope_stage = st.selectbox("Stage", options=["Nothing done", "Read about WBS", "Understand WBS", "Create a WBS", "Get the WBS validated"])
    define_success = st.checkbox("Define project success criteria")
    validate_scope = st.checkbox("Validate scope")
    
    # Section 5
    st.write("5. Time planning")
    time_stage = st.selectbox("Stage", options=["Nothing done", "Read about Gantt Chart", "Understand Gantt Chart", "Create a Gantt Chart", "Get the Gantt Chart validated"])
    
    # Add remaining sections here...
    
    # Submit button
    submitted = st.form_submit_button("Save form")

if submitted:
    
    st.write("Form Submitted!")
    # st.write(f"Team Stage: {team_stage}")
    # st.write(f"Read Project Specification: {spec_read}")
    # st.write(f"Chat with Customer: {chat_customer}")
    # st.write(f"Understand What Need to Do: {understand_need}")
    # st.write(f"Understand What Should Not Do: {understand_not_do}")
    # st.write(f"Describe Functional Requirements: {describe_func_req}")
    # st.write(f"Describe Non-Functional Requirements: {describe_non_func_req}")
    # st.write(f"Scope Stage: {scope_stage}")
    # st.write(f"Define Success Criteria: {define_success}")
    # st.write(f"Validate Scope: {validate_scope}")
    # Include more fields as needed

