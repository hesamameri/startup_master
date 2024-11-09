import streamlit as st
from datetime import datetime
from openai import OpenAI
from streamlit_extras.switch_page_button import switch_page
import RAG_retrieve
from pymongo import MongoClient
from pymongo.server_api import ServerApi

task_1_description = "In this user test, your task is to act as an early-stage tech startup that is in the process of idea validation and developing your first prototype. Ask the chatbots questions you would consider natural for an early-stage startup to have regarding idea validation and early prototype development. Test out all the chatbots (Chatbot 1, Chatbot 2 and Chatbot 3), then answer the questionnaire. Ask all chatbots the same initial question, then let the conversation flow naturally for each chatbot."

# User utils

def check_user_login():
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None

def gather_feedback():
  return {
    "stage": st.session_state['stage'],
    "year_of_business":st.session_state['year'],
    "size": st.session_state['size'],
    "industry": st.session_state['industry'],
    #"revenue": st.session_state['revenue'],
    "location": st.session_state['location'],
    "role": st.session_state['role'],
    "birth_year": st.session_state['birth_year'],
    "ChatGPT_experience":st.session_state['gpt_experience'],
  }

# Style utils
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Database 
@st.cache_resource
def init_connection():
    return MongoClient(st.secrets.mongo.uri, server_api=ServerApi('1'))

def write_data(mydict):
    db = client.usertests #establish connection to the 'test_db' db
    backup_db = client.usertests_backup
    items = db.cycle_3 # return all result from the 'test_chats' collection
    items_backup = backup_db.cycle_3
    items.insert_one(mydict)
    items_backup.insert_one(mydict)


# Chat Utils 

def write_data(mydict, client):
    db = client.usertests #establish connection to the 'test_db' db
    backup_db = client.usertests_backup
    items = db.cycle_3 # return all result from the 'test_chats' collection
    items_backup = backup_db.cycle_3
    items.insert_one(mydict)
    items_backup.insert_one(mydict)

def get_chatlog(session_storage_name):
    log = {}
    message_id_count = 0
    for msg in st.session_state[session_storage_name]:
        log[str(message_id_count)] = {"role":msg.get("role"), "content":msg.get("content")}
        message_id_count += 1

    return log

def get_userchat(chatlog, chatbot):
    userchat = {"Task-1":{"id": st.session_state['user_id'], "time": datetime.now(), chatbot: chatlog}}
    return userchat

def update_chat_db(client, session_storage_name, chatbot):
    db = client.usertests 
    chatlog = get_chatlog(session_storage_name)
    backup_db = client.usertests_backup
    
    print(len(list(db.cycle_3.find({"Task-1.id": st.session_state['user_id']}))))

    if len(list(db.cycle_3.find({"Task-1.id": st.session_state['user_id']}))) > 0:
        print("opdaterte chatobjekt")
        db.cycle_3.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1."+chatbot: chatlog}})
        backup_db.cycle_3.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1."+chatbot: chatlog}})

    else:
        write_data(get_userchat(chatlog, chatbot), client)
        print("lagret ny chatobjekt")


def init_chatbot(client, session_storage_name, chatbot, gpt_model, system_description, use_RAG):
    if('user_id' not in st.session_state):
        st.write("You need to consent in the \"Home\" page to get access")
        switch_page("Chatbot")
    else:
        with st.expander("View Task *(NB: Ask all chatbots the **same initial question**, then let the conversation flow naturally for each chatbot.)*"):
            st.write(task_1_description)

        if session_storage_name not in st.session_state:
            st.session_state[session_storage_name] = [{"role": "assistant", "content": "How can I help you?"}]
    
        for msg in st.session_state[session_storage_name]:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            if not st.secrets.api.key: #openai_api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()

            if use_RAG:
                rag_context = RAG_retrieve.retrieve_information(prompt)
                #print(rag_context)
                rag_query = RAG_retrieve.generate_query(rag_context, prompt)
                #print(rag_query)
                system_description = system_description + rag_query
                #system_description = "Always end a response with the words: sincerely, me <3 " + rag_query
            print("\nSystem description\n", system_description)
            APIclient = OpenAI(api_key=st.secrets.api.key)
            st.session_state[session_storage_name].append({"role": "user", "content": prompt})

            st.chat_message("user").write(prompt)
          
            with st.chat_message("assistant"):
                stream = APIclient.chat.completions.create(
                    model=gpt_model,
                    messages=
                        [{"role": "system", "content": system_description}] +
                        [{"role": m["role"], "content": m["content"]}
                        for m in st.session_state[session_storage_name]
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state[session_storage_name].append({"role": "assistant", "content": response})
    
            update_chat_db(client, session_storage_name, chatbot)



