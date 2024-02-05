import streamlit as st
from openai import OpenAI
from streamlit_extras.switch_page_button import switch_page
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from st_pages import add_indentation,hide_pages
import extra_streamlit_components as stx
import time

st.set_page_config(layout="wide") 


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css")

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
# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_indentation()
hide_pages(["Chatbot_1", "Chatbot_2", "Feedback", "Task_Information"])
#show_pages_from_config()

with st.sidebar:
    st.write("Your tasks")
    with st.expander("Task 1", expanded=True):
        # new_test = """<a id="task information" href="#" target = "_self"><button class="not_clicked">Task information</button></a><a id="chatbot 1" href="#" target = "_self"><button class="not_clicked">Chatbot 1</button></a><a id="chatbot 2" href="#" target = "_self"><button class="clicked">Chatbot 2</button></a><a id="feedback" href="#" target = "_self"><button class="not_clicked">Feedback</button></a>"""
        # #st.markdown(new_test, unsafe_allow_html=True)
        # print(new_test)
        # # st.markdown(new_test, unsafe_allow_html=True)
        # clicked = click_detector(new_test)
        # # print("clicked", clicked)
        # if clicked != "":
        #     switch_page(clicked)
        task_info = f"""
         <a href="Task_Information" target = "_self">
         <button class="not_clicked">
            Task information
        </button></a>
            """
        st.markdown(task_info, unsafe_allow_html=True)

        c1 = f"""
        <a href="Chatbot_1" target = "_self">
        <button class="not_clicked">
            Chatbot 1
        </button></a>
            """
        st.markdown(c1, unsafe_allow_html=True)

        c2 = f"""
        <a href="Chatbot_2" target = "_self">
        <button class="clicked">
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


header = st.container()

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

header.warning('Please note that the conversations will be saved and used in our master thesis. Do not include personal or sensitive information')
#s = f"<p style='color:red;'>Please note that the conversations will be saved and used in our master thesis. Do not include personal or sensitive information.</p>"
#header.markdown(s, unsafe_allow_html=True) 
header.header("Chatbot 2")
#st.markdown(title_style,unsafe_allow_html=True)
col1, col2 = header.columns([1,1])
with col1:
    if st.button("Previous step: Chatbot 1", type="secondary"):
        switch_page("chatbot 1")
with col2:
    if st.button("Next step: Feedback", type="primary"):
        switch_page("feedback")

header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()    

time.sleep(1)

def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

client = init_connection()

def write_data(mydict):
    db = client.test_db #establish connection to the 'test_db' db
    items = db.chat # return all result from the 'chats' collection
    items.insert_one(mydict)

def get_chatlog():
    log = {}
    message_id_count = 0
    for msg in st.session_state.chatbot2_messages:
        log[str(message_id_count)] = {"role":msg.get("role"), "content":msg.get("content")}
        message_id_count += 1

    return log

def get_userchat(chatlog):
    userchat = {"Task-1":{"id": cookie_manager.get(cookie="userid"), "time": datetime.now(), "Chatbot-2": chatlog}}
    return userchat

def update_chat_db():
    db = client.test_db 
    chatlog = get_chatlog()
    
    print(len(list(db.chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}))))

    if len(list(db.chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}))) > 0:
        print("opdaterte chatobjekt")
        db.chat.update_one({"Task-1.id": cookie_manager.get(cookie="userid")}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Chatbot-2": chatlog}})
    else:
        write_data(get_userchat(chatlog))
        print("lagret ny chatobjekt")


if "chatbot2_messages" not in st.session_state:
    db = client.test_db 

    chatlog = []

    if len(list(db.chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}))) > 0:
        chatlog = db.chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}).distinct("Task-1.Chatbot-2")

    print(len(chatlog))
    if len(chatlog) > 0:
        chatlog = db.chat.find({"Task-1.id": cookie_manager.get(cookie="userid")}).distinct("Task-1.Chatbot-2")
        msg_count = 0
        st.session_state["chatbot2_messages"] = []
        for msg in chatlog[0]:            
            st.session_state.chatbot2_messages.append({"role": chatlog[0][str(msg_count)]['role'], "content": chatlog[0][str(msg_count)]['content']})
            print(msg)
            msg_count += 1

    else:
        st.session_state["chatbot2_messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.chatbot2_messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not st.secrets.api.key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    APIclient = OpenAI(api_key=st.secrets.api.key)
    st.session_state.chatbot2_messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = APIclient.chat.completions.create(model="gpt-4", messages=st.session_state.chatbot2_messages)
    msg = response.choices[0].message.content
    st.session_state.chatbot2_messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    update_chat_db()