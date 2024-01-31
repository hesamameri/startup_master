import json
from openai import OpenAI
import streamlit as st
#from streamlit_option_menu import option_menu
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import uuid
from st_pages import add_indentation,hide_pages
import extra_streamlit_components as stx
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout = "wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css")

# Custom CSS for back and forth buttons to fit content
st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

### Custom CSS for the sticky header
st.markdown(
    """
<style>
    div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
        position: sticky;
        top: 2.875rem;
        background-color: white;
        z-index: 999;
    }
</style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)



####### SIDEBAR #######
add_indentation()
hide_pages(["Chatbot_1", "Chatbot_2", "Feedback", "Task_Information"])

with st.sidebar:
    st.write("Your tasks")
    with st.expander("Task 1", expanded=True):
        task_info = f"""
        <a href="Task_Information" target = "_self">
        <button class="not_clicked">
            Task information
        </button></a>
            """
        st.markdown(task_info, unsafe_allow_html=True)
        
        c1 = f"""
        <a href="Chatbot_1" target = "_self">
        <button class="clicked">
            Chatbot 1
        </button></a>
            """
        st.markdown(c1, unsafe_allow_html=True)

        c2 = f"""
        <a href="Chatbot_2" target = "_self">
        <button class="not_clicked">
            Chatbot 2
        </button></a>
            """
        st.markdown(c2, unsafe_allow_html=True)

        feedback = f"""
        <a href="Feedback" target = "_self">
        <button class="not_clicked">
            Feedback
        </button></a>
            """
        st.markdown(feedback, unsafe_allow_html=True)

### HEADER ###
header = st.container()
header.warning('Please note that the conversations will be saved and used in our master thesis. Do not include personal or sensitive information')
header.header("Chatbot 1")
col1, col2 = header.columns([1,1])
with col1:
    if st.button("Previous step: Task Information", type="secondary"):
        switch_page("task information")
with col2:
    if st.button("Next step: Chatbot 2", type="primary"):
        switch_page("chatbot 2")

header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)



### MAIN CONTENT ###
# Generate a random UUID (UUID4)
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = str(uuid.uuid4())
    print(st.session_state.user_id)

@st.cache_resource
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

# #st.subheader("All Cookies:")
# cookies = cookie_manager.get_all()
# #st.write(cookies)
# print(cookies)

# # @st.cache_resource
# # def get_manager():
# #     return stx.CookieManager()

# cookie_manager = get_manager()
# # Generate a random UUID (UUID4)
# if 'user_id' not in st.session_state:
#     if len(cookie_manager.get(cookie="userid")) == 0:
#         print("her")
#         st.session_state['user_id'] = str(uuid.uuid4())
#         #cookie = st.text_input("Cookie", key="1")
#         cookie_manager.set("userid", st.session_state.user_id)
    
#     else:
#         st.session_state['user_id'] = cookie_manager.get(cookie="userid")
#     #cookie2 = st.text_input("Cookie", key="0")
#     # print("kjeksoppskrift:")
#     # all_cookies = cookie_manager.get_all()
#     # print("starter klokke")
#     # time.sleep(2)
#     # print("klokke ferdig")

#     # print(all_cookies)
#     # print(cookie_manager.get(cookie="userid"))
#     # print(st.session_state.user_id)
#user_id = uuid.uuid4()
# st.session_state['user_id'] = cookie_manager.get(cookie="userid")
# print(cookie_manager.get(cookie="userid"))
# print(st.session_state.user_id)

def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()

def write_data(mydict):
    db = client.test_db #establish connection to the 'test_db' db
    items = db.test_chat # return all result from the 'test_chats' collection
    items.insert_one(mydict)

def get_chatlog():
    log = {}
    message_id_count = 0
    for msg in st.session_state.chatbot1_messages:
        log[str(message_id_count)] = {"role":msg.get("role"), "content":msg.get("content")}
        message_id_count += 1

    return log

def get_userchat(chatlog):
    userchat = {"Task-1":{"id": cookie_manager.get(cookie="userid"), "time": datetime.now(), "Chatbot-1": chatlog}}
    return userchat

def update_chat_db():
    db = client.test_db 
    chatlog = get_chatlog()
    
    print(len(list(db.test_chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}))))

    if len(list(db.test_chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}))) > 0:
        print("opdaterte chatobjekt")
        db.test_chat.update_one({"Task-1.id": cookie_manager.get(cookie="userid")}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Chatbot-1": chatlog}})
    else:
        write_data(get_userchat(chatlog))
        print("lagret ny chatobjekt")


if "chatbot1_messages" not in st.session_state:
    db = client.test_db 
    chatlog = []

    if len(list(db.test_chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}))) > 0:
        chatlog = db.test_chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}).distinct("Task-1.Chatbot-1")

    print(len(chatlog))
    if len(chatlog) > 0:
        chatlog = db.test_chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}).distinct("Task-1.Chatbot-1")
        msg_count = 0
        st.session_state["chatbot1_messages"] = []
        for msg in chatlog[0]:
            st.session_state.chatbot1_messages.append({"role": chatlog[0][str(msg_count)]['role'], "content": chatlog[0][str(msg_count)]['content']})
            print(msg)
            msg_count += 1

    else:
        st.session_state["chatbot1_messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.chatbot1_messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    #client = OpenAI(api_key=openai_api_key)
    st.session_state.chatbot1_messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    #response = client.chat.completions.create(model="gpt-3.5-turbo", chatbot1_messages=st.session_state.chatbot1_messages)
    msg = "hello" #response.choices[0].message.content
    st.session_state.chatbot1_messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    
    print("kjeks her:", cookie_manager.get(cookie="userid"))

    update_chat_db()

