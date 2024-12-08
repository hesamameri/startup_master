from datetime import datetime
import pymongo
import streamlit as st
import extra_streamlit_components as stx
import time
from streamlit_extras.switch_page_button import switch_page
st.set_page_config(layout="wide")
from auth import log_out 
import openai
# st.sidebar.page_link('pages/Project_Buddy.py', label='Project Buddy')
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

        with st.sidebar.expander("Project Buddy", expanded=False):
            for date, chats_for_date in sorted(grouped_chats.items(), key=lambda item: item[0], reverse=True):
                st.markdown(f"### {date.strftime('%A, %B %d, %Y')}")  # Display date header
                for chat in chats_for_date:
                    if st.button(chat['title']):
                        st.session_state['chat_id'] = chat['chat_id']
                        st.session_state['chat_activated'] = True
                        st.switch_page('pages/Project_Buddy.py')

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
                for date, chats_for_date in sorted(grouped_chats.items(), key=lambda item: item[0], reverse=True):
                    st.markdown(f"### {date.strftime('%A, %B %d, %Y')}")  # Display date header
                    for chat in chats_for_date:
                        if st.button(chat['title']):
                            st.session_state['chat_id'] = chat['chat_id']
                            st.session_state['chat_activated'] = True
                            st.switch_page('pages/Project_Buddy.py')

        else:
            print("H works")
            st.sidebar.page_link('pages/Project_Buddy.py', label='Project Buddy')

#################
st.sidebar.page_link('pages/Getting_Feedback.py', label='Getting Feedback')
st.sidebar.page_link('pages/Your_Progress.py', label='Your Progress')

st.sidebar.page_link('pages/Keeping_Track.py', label='Keeping Track')
st.sidebar.page_link('pages/Meeting_Room.py', label='Meeting Room')
if st.sidebar.button("Log Out"):
    log_out()  # Call the log_out function when the button is clicked


st.header("Summary of your team progress")

today = date.today()
st.write("Here we summarize your learning progress up to ", today)

my_coursetime = st.progress(20, text="You have completed 3/ 15 study weeks of this course")
my_assignment = st.progress(20, text="You have completed 5/ 25 exercises in this course")
my_milestones = st.progress(33, text="You have completed 1/ 3 obligatory milestones in this course")
my_meeting = st.progress(33, text="You have completed 1/ 10 obligatory meetings in this course")
my_agile = st.progress(33, text="You have completed 5/ 10 suggested Agile practices in this course")
my_product = st.progress(10, text="You have completed 2/ 20 requirements in this course")

st.write("Here is our feedback on your progress")

st.write("Team: It looks like you have established your team! Do you get more meeting with other team members? Have you considered using a team contract to improve commitment within the team?")
st.write("Customer: Here is the summary of your conversation with the customer so far. Make sure the request from the customers correctly understood!")
st.write("Knowledge module: At this time, you should have completed module 2 with creating WBS for your project. Are you not sure if it is not correct? Send an email to the lecturer for feedback: anguatusn.no")
st.write("Process: Do you define how you and teammates will work together? We suggest to follow Scrum method. Let start the first Srpint. More information, read Module 4")
st.write("Product: It is still early to work with the website now. However, you might want to look at websites about HTML, CSS to learn about web development!")
st.write("Report: It is early to work with the report now. Obligagory Assignment 1 is the closet formal milestone.")

