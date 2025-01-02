import openai
import pymongo
import streamlit as st
import extra_streamlit_components as stx
import time
from streamlit_extras.switch_page_button import switch_page
from datetime import date, datetime, timedelta
from pymongo import MongoClient
from auth import log_out
import streamlit as st
import pymongo
from datetime import datetime
from bson import ObjectId

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



######################################### MAIN PAGE

st.header("Følger fremgangen din her!")
st.write("Du må registrere fremgangen din ved å fylle ut skjemaet nedenfor når foreleseren får beskjed om det. Du må fylle den nøye og ærlig for å få den mest passende tilbakemeldingen for prosjektet ditt. Hent først det siste skjemaet (hvis noen), og begynn å fylle ut eller redigere skjemaet. Når du er ferdig klikker du på send for å sende skjemaet til foreleseren.")


# MongoDB connection setup
connection_string = st.secrets['mongo']['uri']
client = pymongo.MongoClient(connection_string)
db = client['users']
destination_collection = db["projects"]
user_collection = db['usertests']

username = st.session_state['username']  # Use 'username' instead of 'user_id'

user_class = user_collection.find_one({"username": username}).get("class")
# Initialize session state for retrieved data
if "retrieved_data" not in st.session_state:
    st.session_state["retrieved_data"] = {}

# Button to retrieve the latest form data
if st.button("Hent det siste skjemaet"):
    # Fetch the user data
    user_data = destination_collection.find_one({"username": username})  # Query by 'username'
    
    if user_data:
        # Sort the forms by timestamp to get the latest one
        latest_form = max(user_data["forms"], key=lambda x: x["timestamp"])
        st.session_state["retrieved_data"] = latest_form
        st.success("Det siste fremdriftsskjemaet er hentet!")
    else:
        st.warning("Det er ikke registrert skjema fra før. Du kan starte din første fremdriftsundersøkelse nå!")

# Display the form
with st.form("this"):
    # Populate form fields with retrieved data or default values
    st.write("1. Team Formation")
    team_stage = st.selectbox(
        "Team Stage",
        options=['Found a team', 'Understand'],
        index=['Found a team', 'Understand'].index(
            st.session_state["retrieved_data"].get("TeamStage", "Found a team")
        )
    )
    st.write("2. Requirement Engineering")
    project_spec_read = st.checkbox("Read Project Specification", value=st.session_state["retrieved_data"].get("ProjectSpecRead", False))
    project_spec_chat = st.checkbox("Chat with the customer?", value=st.session_state["retrieved_data"].get("ProjectSpecChat", False))
    project_spec_understood = st.checkbox("Understand what to do and not?", value=st.session_state["retrieved_data"].get("ProjectSpecUnderstood", False))
    project_func_req = st.checkbox("Describe functional requirements", value=st.session_state["retrieved_data"].get("ProjectFuncReq", False))
    project_nonfunc_req = st.checkbox("Describe non-functional requirements", value=st.session_state["retrieved_data"].get("ProjectNonFuncReq", False))
    st.write("3. Configuration Management")
    tool_repo = st.checkbox("Set up a project repository - Github, Dropbox, etc", value=st.session_state["retrieved_data"].get("ToolRepo", False))
    tool_comm = st.checkbox("Set up a communication tool - Team, Slack, etc", value=st.session_state["retrieved_data"].get("ToolComm", False))
    tool_mngt = st.checkbox("Set up a project management tool - Trello, Monday, etc", value=st.session_state["retrieved_data"].get("ToolMngt", False))
    tool_ides = st.checkbox("Set up a development environments - Visual Studio, Wix, etc", value=st.session_state["retrieved_data"].get("ToolIDEs", False))
    tool_mvps = st.checkbox("Set up a prototyping tool - Figma", value=st.session_state["retrieved_data"].get("ToolMVPs", False))
    tool_docs = st.checkbox("Set up a collaborative documenting tool - Google Doc, Word 365, etc", value=st.session_state["retrieved_data"].get("ToolDocs", False))
    tool_innspill = st.checkbox("Set up account to InnSpill AI", value=st.session_state["retrieved_data"].get("ToolInnspill", False))
    st.write("4. Scope and Time Management")
    wbs = st.selectbox(
        "WBS",
        options=['Not done', 'WBS is created', 'WBS is validated'],
        index=['CreateNoWBS', 'CreateWBS', 'ValidateWBS'].index(
            st.session_state["retrieved_data"].get("WBS", "CreateNoWBS")
        )
    )  
    time_estimated = st.checkbox("Time Estimated for Activities ?", value=st.session_state["retrieved_data"].get("TimeEstimated", False))
    ganttchart = st.selectbox(
        "GanttChart",
        options=['Not done', 'Gantt Chart is created', 'Gantt Chart is validated'],
        index=['CreateNoGantt', 'CreateGantt', 'ValidateGantt'].index(
            st.session_state["retrieved_data"].get("GanttChart", "CreateNoGantt")
        )
    )      
    st.write("5. Risk and Communication Management")
    risk_table = st.checkbox("Develop a risk table and calculate risk score", value=st.session_state["retrieved_data"].get("RiskTable", False))
    risk_resolved = st.checkbox("Develop countermeasure for all risk items", value=st.session_state["retrieved_data"].get("RiskResolved", False))
    role_defined = st.checkbox("Define all roles in the project?", value=st.session_state["retrieved_data"].get("RoleDefined", False))
    task_assigned = st.checkbox("Assign tasks for all member in the project?", value=st.session_state["retrieved_data"].get("TaskAssigned", False))
    communication_plan = st.checkbox("Develop a communication plan for the project", value=st.session_state["retrieved_data"].get("CmmPlan", False))

    st.write("6. Prototyping")
    prototype_low = st.checkbox("Create a low-fidelity prototype with paper and pen", value=st.session_state["retrieved_data"].get("PrototypeLow", False))
    prototype_high = st.checkbox("Create a high-fidelity prototype with Figma", value=st.session_state["retrieved_data"].get("PrototypeHigh", False))
    prototype_website = st.checkbox("Create a functional website", value=st.session_state["retrieved_data"].get("PrototypeWebsite", False))
    prototype_law = st.checkbox("Learn about UX law for design - Gestal Law, WCAG, etc", value=st.session_state["retrieved_data"].get("PrototypeLaw", False))

    st.write("7. Agile Development")
    agile_user_stories = st.checkbox("Use user stories for requirement documentation", value=st.session_state["retrieved_data"].get("AgileUserStories", False))
    agile_product_backlog = st.checkbox("Create a product backlog", value=st.session_state["retrieved_data"].get("AgileProductBacklog", False))
    agile_sprint_backlog = st.checkbox("Create a Sprint backlog", value=st.session_state["retrieved_data"].get("AgileSprintBacklog", False))
    agile_backlog_assigned = st.checkbox("Assign backlog items to a person", value=st.session_state["retrieved_data"].get("AgileBacklogAssigned", False))
    agile_kanban = st.checkbox("Setup Kanban board with ToDo, Doing and Done columns?", value=st.session_state["retrieved_data"].get("AgileKanban", False))
    agile_meeting_planning = st.checkbox("Conduct a Sprint planning meeting?", value=st.session_state["retrieved_data"].get("AgileSprintPlanning", False))
    agile_meeting_review = st.checkbox("Conduct a Sprint review meeting?", value=st.session_state["retrieved_data"].get("AgileSprintReview", False))
    agile_meeting_retro = st.checkbox("Conduct a Sprint retrospective meeting?", value=st.session_state["retrieved_data"].get("AgileSprintRetroSpective", False))

    st.write("8. Solution Design")
    technical_solution = st.checkbox("Do you decide technologies, frameworks or tools to implement the website?", value=st.session_state["retrieved_data"].get("TechnicalSolution", False))
    architectural_design = st.checkbox("Do you decide or know about the architecture of the website?", value=st.session_state["retrieved_data"].get("ArchitecturalDesign", False))

    st.write("9. Testing")
    test_plan = st.checkbox("Do you have an overall test plan?", value=st.session_state["retrieved_data"].get("TestPlan", False))
    test_case = st.checkbox("Do you have all test cases you need?", value=st.session_state["retrieved_data"].get("TestCase", False))
    test_usability = st.checkbox("Do you have an usability testing plan?", value=st.session_state["retrieved_data"].get("TestUsability", False))
    test_result = st.checkbox("Do you document the test result?", value=st.session_state["retrieved_data"].get("TestResult", False))

    st.write("10. Project Closing")
    project_report = st.checkbox("Do you finish your final report?", value=st.session_state["retrieved_data"].get("ProjectReport", False))
    project_website = st.checkbox("Do you have the website ready for demo?", value=st.session_state["retrieved_data"].get("ProjectWebsite", False))
    project_oblig = st.checkbox("Do you check that all Obligs are approved?", value=st.session_state["retrieved_data"].get("ProjectOblig", False))
    project_tool_closed = st.checkbox("Do you finalize or close your working spaces with tools?", value=st.session_state["retrieved_data"].get("ProjectToolClosed", False))
    project_midterm_slide = st.checkbox("Do you have the midterm presentation slide?", value=st.session_state["retrieved_data"].get("SlideMidterm", False))
    project_final_slide = st.checkbox("Do you have the final presentation slide?", value=st.session_state["retrieved_data"].get("SlideFinal", False))
    submitted_form = st.form_submit_button("Save form")
    
    # Submit button to insert or update values in the database
    if submitted_form:
        # Collect the values into a dictionary for database insertion or update
        new_form_data = {
            "TeamStage": team_stage,
            "ProjectSpecRead": project_spec_read,
            "ProjectSpecChat": project_spec_chat,
            "ProjectSpecUnderstood": project_spec_understood,
            "ProjectFuncReq": project_func_req,
            "ProjectNonFuncReq": project_nonfunc_req,
            "ToolRepo": tool_repo,
            "ToolComm": tool_comm,
            "ToolMngt": tool_mngt,
            "ToolIDEs": tool_ides,
            "ToolMVPs": tool_mvps,
            "ToolDocs": tool_docs,
            "ToolInnspill": tool_innspill,
            "WBS": wbs,
            "TimeEstimated": time_estimated,
            "GanttChart": ganttchart,
            "RiskTable": risk_table,
            "RiskResolved": risk_resolved,
            "RoleDefined": role_defined,
            "TaskAssigned": task_assigned,
            "CmmPlan": communication_plan,
            "PrototypeLow": prototype_low,
            "PrototypeHigh": prototype_high,
            "PrototypeWebsite": prototype_website,
            "PrototypeLaw": prototype_law,
            "AgileUserStories": agile_user_stories,
            "AgileProductBacklog": agile_product_backlog,
            "AgileSprintBacklog": agile_sprint_backlog,
            "AgileBacklogAssigned": agile_backlog_assigned,
            "AgileKanban": agile_kanban,
            "AgileSprintPlanning": agile_meeting_planning,
            "AgileSprintReview": agile_meeting_review,
            "AgileSprintRetroSpective": agile_meeting_retro,
            "TechnicalSolution": technical_solution,
            "ArchitecturalDesign": architectural_design,
            "TestPlan": test_plan, 
            "TestCase": test_case,
            "TestUsability": test_usability,
            "TestResult": test_result,
            "ProjectReport": project_report,
            "ProjectWebsite": project_website,
            "ProjectOblig": project_oblig,
            "ProjectToolClosed": project_tool_closed,
            "SlideMidterm": project_midterm_slide,
            "SlideFinal": project_final_slide,
            "timestamp": datetime.now()  # Set the current timestamp
        }

        # Check if the user has any existing project records
        existing_record = destination_collection.find_one({"username": username})

        if existing_record:
            # Add the new form to the existing user's forms array
            destination_collection.update_one(
                {"username": username},
                {"$push": {"forms": new_form_data}}  # Append the new form to the 'forms' array
            )
            st.success("Form added successfully!")
        else:
            # Create a new record with the user and the first form entry
            print(user_class)
            new_user_data = {
                "username": username,
                "selected_class": user_class,  # Add the default class if needed
                "forms": [new_form_data]  # Create the first form entry
            }
            result = destination_collection.insert_one(new_user_data)
            st.success(f"Form submitted successfully! Document ID: {result.inserted_id}")

        # Clear session state items
        if "retrieved_data" in st.session_state:
            del st.session_state["retrieved_data"]






    

