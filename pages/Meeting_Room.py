import openai
import pymongo
import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
import app_components as components
from auth import log_out 
from datetime import datetime
st.set_page_config(layout = "wide", page_title="Customer Meeting")
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

########################


# MongoDB connection setup
connection_string = st.secrets['mongo']['uri']
client = pymongo.MongoClient(connection_string)
db = client['users']
collection = db["meeting"]

# OpenAI API key setup
openai.api_key = st.secrets["api"]["key"]

# Function to get the active meeting type
def get_active_meeting_type():
    document = collection.find_one()  # Assuming there's only one document
    if document and "meetings" in document:
        for meeting in document["meetings"]:
            if meeting.get("active") == 1:
                return meeting.get("Meet_type")
    return None

# Function to generate feedback using ChatGPT
def generate_feedback(user_response):
    try:
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing feedback."},
                {"role": "user", "content": user_response},
            ]
        )
        feedback = completion.choices[0].message.content
        return feedback
    except Exception as e:
        st.error(f"Error generating feedback: {e}")
        return "Error: Unable to generate feedback."

# Fetch the active meeting type
active_meeting_type = get_active_meeting_type()

# Display content only if the active meeting type is "customermeeting"
if active_meeting_type == "customermeeting":
    # Center and style the header and image
    st.markdown("""
        <div style="text-align: center;">
            <h1>Reidar Hellegurd</h1>
            <img src="https://www.nih.no/om/ansatte/reidars/reidar_safvenbom_250x250.jpg" width="200" style="border-radius: 50%;">
        </div>
    """, unsafe_allow_html=True)

    # Add markdown content with enhanced readability
    st.markdown("""
        The meetings with customers are scheduled. Today you will talk to your Customer Reidar Hellegurd.
        The objective of the meeting is to clarify the customer's need. Read the project description and prepare your questions.
        An example of questions can be - What is the preferred color scheme for the home page? How the cover photo should look like?
    """, unsafe_allow_html=False)

    username = st.session_state['username'] # Replace 'default_user' with a logic for the current user

    # Initialize chat state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Check if a chat record exists for the given username and meet_type
    chat_record = collection.find_one({"username": username, "meet_type": active_meeting_type})

    # Update session state with existing chat history
    if chat_record and "chat" in chat_record:
        st.session_state["chat_history"] = chat_record["chat"]

    # Placeholder for chat history
    chat_placeholder = st.empty()

    # Display chat history
    with chat_placeholder.container():
        st.markdown("### Previous Conversations")
        for entry in st.session_state["chat_history"]:
            st.markdown(f"**You:** {entry['response']}")
            st.markdown(f"**Assistant:** {entry['feedback']}")
            st.markdown("---")

    # Form for new input with styling
    
    with st.form("chat_form"):
        user_response = st.text_area("Write your question here", "", height=70, key="question_input", placeholder="Type your question here...")
        submitted = st.form_submit_button("Submit")

        # Handle form submission
        if submitted:
            if not username or not user_response:
                st.warning("Please provide a message.")
            else:
                # Generate feedback using ChatGPT
                feedback = generate_feedback(user_response)

                new_entry = {"response": user_response, "feedback": feedback}

                if chat_record:
                    # Update existing chat record
                    collection.update_one(
                        {"_id": chat_record["_id"]},
                        {"$push": {"chat": new_entry}}
                    )
                else:
                    # Create a new chat record
                    new_chat = {
                        "username": username,
                        "meet_type": active_meeting_type,
                        "chat": [new_entry]
                    }
                    collection.insert_one(new_chat)

                # Update session state and re-render chat
                st.session_state["chat_history"].append(new_entry)
                chat_placeholder.empty()
                with chat_placeholder.container():
                    st.markdown("### Previous Conversations")
                    for entry in st.session_state["chat_history"]:
                        st.markdown(f"**You:** {entry['response']}")
                        st.markdown(f"**Assistant:** {entry['feedback']}")
                        st.markdown("---")

                st.success("Your question and feedback have been added.")
else:
    # Message for when the active meeting type is not "customermeeting"
    st.warning("No customer meeting is currently active.")

# # MongoDB connection setup
# connection_string = st.secrets['mongo']['uri']
# client = pymongo.MongoClient(connection_string)
# db = client['users']
# collection = db["meeting"]

# # OpenAI API key setup
# openai.api_key = st.secrets["api"]["key"]

# # Function to get the active meeting type
# def get_active_meeting_type():
#     document = collection.find_one()  # Assuming there's only one document
#     if document and "meetings" in document:
#         for meeting in document["meetings"]:
#             if meeting.get("active") == 1:
#                 return meeting.get("Meet_type")
#     return None

# # Function to generate feedback using ChatGPT
# def generate_feedback(user_response):
#     try:
#         completion = openai.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant providing feedback."},
#                 {"role": "user", "content": user_response},
#             ]
#         )
#         feedback = completion.choices[0].message.content
#         return feedback
#     except Exception as e:
#         st.error(f"Error generating feedback: {e}")
#         return "Error: Unable to generate feedback."

# # Fetch the active meeting type
# active_meeting_type = get_active_meeting_type()

# # Display content only if the active meeting type is "customermeeting"
# if active_meeting_type == "customermeeting":
#     # Center and style the header and image
#     st.markdown("""
#         <div style="text-align: center;">
#             <h1>Reidar Hellegurd</h1>
#             <img src="https://www.nih.no/om/ansatte/reidars/reidar_safvenbom_250x250.jpg" width="200" style="border-radius: 50%;">
#         </div>
#     """, unsafe_allow_html=True)

#     # Add markdown content with enhanced readability
#     st.markdown("""
#         The meetings with customers are scheduled. Today you will talk to your Customer Reidar Hellegurd.
#         The objective of the meeting is to clarify the customer's need. Read the project description and prepare your questions.
#         An example of questions can be - What is the preferred color scheme for the home page? How the cover photo should look like?
#     """, unsafe_allow_html=False)

#     username = st.session_state['username'] # Replace 'default_user' with a logic for the current user

#     # Check if a chat record exists for the given username and meet_type
#     chat_record = collection.find_one({"username": username, "meet_type": active_meeting_type})

#     # Display previous chats if available
#     if chat_record and "chat" in chat_record:
#         st.markdown("### Previous Conversations")
#         for entry in chat_record["chat"]:
#             st.markdown(f"**You:** {entry['response']}")
#             st.markdown(f"**Assistant:** {entry['feedback']}")
#             st.markdown("---")

#     # Form for new input with styling
#     st.markdown("### Start a New Conversation")
#     with st.form("chat_form"):
#         user_response = st.text_area("Write your question here", "", height=70, key="question_input", placeholder="Type your question here...")
#         submitted = st.form_submit_button("Submit")

#         # Handle form submission
#         if submitted:
#             if not username or not user_response:
#                 st.warning("Please provide a message.")
#             else:
#                 # Generate feedback using ChatGPT
#                 feedback = generate_feedback(user_response)

#                 if chat_record:
#                     # Update existing chat record
#                     collection.update_one(
#                         {"_id": chat_record["_id"]},
#                         {"$push": {"chat": {"response": user_response, "feedback": feedback}}}
#                     )
#                     st.success("Your question and feedback have been added to the existing chat record.")
#                 else:
#                     # Create a new chat record
#                     new_chat = {
#                         "username": username,
#                         "meet_type": active_meeting_type,
#                         "chat": [
#                             {
#                                 "response": user_response,
#                                 "feedback": feedback
#                             }
#                         ]
#                     }
#                     collection.insert_one(new_chat)
#                     st.success("A new chat record has been created with your question and feedback.")
# else:
#     # Message for when the active meeting type is not "customermeeting"
#     st.warning("No customer meeting is currently active.")



# connection_string = st.secrets['mongo']['uri']
# client = pymongo.MongoClient(connection_string)
# db = client['users']
# collection = db["meeting"]
# openai.api_key = st.secrets["api"]["key"]

# # Function to get active meeting type
# def get_active_meeting_type():
#     document = collection.find_one()  # Assuming there's only one document
#     if document and "meetings" in document:
#         for meeting in document["meetings"]:
#             if meeting.get("active") == 1:
#                 return meeting.get("Meet_type")
#     return None

# # Function to generate feedback using ChatGPT
# def generate_feedback(user_response):
#     try:
#         completion = openai.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant providing feedback."},
#                 {"role": "user", "content": user_response},
#             ]
#         )
#         feedback = completion.choices[0].message.content
#         return feedback
#     except Exception as e:
#         st.error(f"Error generating feedback: {e}")
#         return "Error: Unable to generate feedback."

# # Fetch the active meeting type
# active_meeting_type = get_active_meeting_type()

# # Display content only if the active meeting type is "customermeeting"
# if active_meeting_type == "customermeeting":
#     # Center and style the header and image
#     st.markdown("""
#         <div style="text-align: center;">
#             <h1>Reidar Hellegurd</h1>
#             <img src="https://www.nih.no/om/ansatte/reidars/reidar_safvenbom_250x250.jpg" width="200" style="border-radius: 50%;">
#         </div>
#     """, unsafe_allow_html=True)

#     # Add markdown content with enhanced readability
#     st.markdown("""
#         The meetings with customers are scheduled. Today you will talk to your Customer Reidar Hellegurd.
#         The objective of the meeting is to clarify the customer's need. Read the project description and prepare your questions.
#         An example of questions can be - What is the preferred color scheme for the home page? How the cover photo should look like?
#     """, unsafe_allow_html=False)

#     # Form for input with styling
#     with st.form("chat_form"):
#         username = st.session_state['username']
#         user_response = st.text_area("Write your question here", "", height=70, key="question_input", placeholder="Type your question here...")
#         submitted = st.form_submit_button("Submit")

#         # Handle form submission
#         if submitted:
#             if not username or not user_response:
#                 st.warning("Please provide a message.")
#             else:
#                 # Check if a chat record exists for the given username and meet_type
#                 chat_record = collection.find_one({"username": username, "meet_type": active_meeting_type})

#                 # Generate feedback using ChatGPT
#                 feedback = generate_feedback(user_response)

#                 if chat_record:
#                     # Update existing chat record
#                     collection.update_one(
#                         {"_id": chat_record["_id"]},
#                         {"$push": {"chat": {"response": user_response, "feedback": feedback}}}
#                     )
#                     st.success("Your question and feedback have been added to the existing chat record.")
#                 else:
#                     # Create a new chat record
#                     new_chat = {
#                         "username": username,
#                         "meet_type": active_meeting_type,
#                         "chat": [
#                             {
#                                 "response": user_response,
#                                 "feedback": feedback
#                             }
#                         ]
#                     }
#                     collection.insert_one(new_chat)
#                     st.success("A new chat record has been created with your question and feedback.")
# else:
#     # Message for when the active meeting type is not "customermeeting"
#     st.warning("No customer meeting is currently active.")



# # Center and style the header and image
# st.markdown("""
#     <div style="text-align: center;">
#         <h1>Reidar Hellegurd</h1>
#         <img src="https://www.nih.no/om/ansatte/reidars/reidar_safvenbom_250x250.jpg" width="200" style="border-radius: 50%;">
#     </div>
# """, unsafe_allow_html=True)

# # Add markdown content with enhanced readability
# st.markdown("""
#     The meetings with customers are scheduled. Today you will talk to your Customer Reidar Hellegurd.
#     The objective of the meeting is to clarify the customer's need. Read the project description and prepare your questions.
#     An example of questions can be - What is the preferred color scheme for the home page? How the cover photo should look like?
# """, unsafe_allow_html=False)

# # Form for input with styling
# with st.form("my_form"):
#     jim_line = st.text_area("Write your question here", "", height=70, key="question_input", placeholder="Type your question here...")
#     submitted = st.form_submit_button("Submit")

#     # Optional: Confirmation message after submission
#     if submitted:
#         st.success("Your question has been submitted successfully!")



