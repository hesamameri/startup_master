import openai
import pymongo
import streamlit as st
import extra_streamlit_components as stx
import time
from streamlit_extras.switch_page_button import switch_page
from datetime import date, datetime, timedelta

from auth import log_out


st.set_page_config(layout="wide") 
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

        with st.sidebar.expander("Project Buddy", expanded=False):
            for date, chats_for_date in grouped_chats.items():
                st.markdown(f"### {date.strftime('%A, %B %d, %Y')}")  # Display date header
                for chat in chats_for_date:
                    if st.button(chat['title']):
                        st.session_state['chat_id'] = chat['chat_id']
                        st.session_state['chat_activated'] = True

    else:
        print("C works")
        st.sidebar.page_link('pages/Project_Buddy.py', label='Project Buddy')

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

            with st.sidebar.expander("Project Buddy", expanded=False):
                for date, chats_for_date in grouped_chats.items():
                    st.markdown(f"### {date.strftime('%A, %B %d, %Y')}")  # Display date header
                    for chat in chats_for_date:
                        if st.button(chat['title']):
                            st.session_state['chat_id'] = chat['chat_id']
                            st.session_state['chat_activated'] = True

        else:
            print("H works")
            st.sidebar.page_link('pages/Project_Buddy.py', label='Project Buddy')

  



            
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
      st.caption("Milestone 1 - Project planning")
      st.write("1. Team formation")
      st.selectbox("Stage", options=["No team found", "Found a team", "Agree on way of working", "Storming time", "Performing time"], placeholder="Select an option", index=None)
      st.write("2. Project specification")
      st.checkbox("Read project specification")
      st.checkbox("Chat with the customer")
      st.checkbox("Understand what need to do")
      st.checkbox("Understand what should not do")
      st.checkbox("Describe the functional requirements")
      st.checkbox("Describe the non-functional requirements")
      st.write("3. Tool and Configuration") 
      st.checkbox("Set up a project repository - Github, Dropbox, etc")
      st.checkbox("Set up communication tool - Team, Messenger, Slack, etc")
      st.checkbox("Set up a project management board - Trello, Monday, etc")
      st.checkbox("Set up a software development environment - Visual Studio, Sublime, etc")
      st.checkbox("Set up a document editor tool - Word 365, Google Doc, etc")
      st.checkbox("Learn to use LearnIX")
      st.write("4. Scope planning")
      st.selectbox("Stage", options=["Nothing done", "Read about WBS", "Understand WBS", "Create a WBS", "Get the WBS validated"], placeholder="Select an option", index=None)
      st.checkbox("Define project success criteria")
      st.checkbox("Validate scope")
      st.write("5. Time planning")
      st.selectbox("Stage", options=["Nothing done", "Read about Gantt Chart", "Understand Gantt Chart", "Create a Gantt Chart", "Get the Gantt Chart validated"], placeholder="Select an option", index=None)
      st.write("6. Risk management")
      st.checkbox("Develop a risk table and calcualte risk score")
      st.checkbox("Develop a countermeasurement for risk items")
      st.write("7. Communication management")
      st.checkbox("Define roles in the projects")
      st.checkbox("Develop a communication plan table")
      st.caption("Milestone 2 - Project execution")
      st.write("8. Prototyping")
      st.checkbox("Create a low-fidelity prototype with paper and pen")
      st.checkbox("Create a low-fidelity prototype with Figma")
      st.checkbox("Create a high-fidelity prototype with Figma")
      st.checkbox("Create a high-fidelity prototype with functional website")
      st.checkbox("Learn about UX law for design: Gestalt law, Universial Design, WCAG")
      st.write("9. Agile development")
      st.checkbox("Use user stories for requirement documentation")
      st.checkbox("Create a product backlog")
      st.checkbox("Estimate priority of product backlog items")
      st.checkbox("Estimate effort for doing product backlog items")
      st.checkbox("Create a Sprint backlog")
      st.checkbox("Create a Burndown Chart")
      st.checkbox("Set up Kanban columns with ToDo, Doing and Done?")
      st.checkbox("Perform a Sprint planning meeting")
      st.checkbox("Have a list of Definition of Done for Sprint?")
      st.checkbox("Perform a Sprint review meeting")
      st.checkbox("Perform a Sprint retrospective meeting")
      st.write("10. Software product design")
      st.checkbox("Use UML diagrams like use case diagram, class diagram, activity diagram, etc")
      st.checkbox("Define the technological approach and technological stack, i.e. wix, Wordpress, HTML, netlify, etc")
      st.checkbox("Study the architecture of the web with the selected technological approach")
      st.checkbox("11. Software implementation")
      st.checkbox("Write code with HTML and CSS")
      st.checkbox("Write code with Javascript")
      st.checkbox("Write backend code with i.e. PHP, Python, C#, ...")
      st.checkbox("Install a database with i.e. MySQL, SQLServer, MongoDB, etc")
      st.write("12. Testing")
      st.checkbox("Learn about unit test, component test and customer test")
      st.checkbox("Develop a test plan")
      st.checkbox("Execute the test plan")
      st.checkbox("Develop a usability test plan")
      st.checkbox("Execute the usability test plan")
      st.write("13. Deployment")
      st.checkbox("Organize Github folder")
      st.checkbox("Format all reports")
      st.checkbox("Create final presentation and practice")
      st.form_submit_button("Save form")

