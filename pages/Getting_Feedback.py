from datetime import datetime
import pymongo
import streamlit as st
from openai import OpenAI
import os
#from decouple import config
import openai
import streamlit as st
#from streamlit_chat import message
from email.policy import default
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from auth import log_out
st.set_page_config(layout = "wide", page_title="StartupGPT")
#import app_components as components 
#import chatbot_utils as cu

# client = OpenAI(api_key=st.secrets["OPENAI_KEY"])
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

  



            
st.sidebar.page_link('pages/Getting_Feedback.py', label='Getting Feedback')
st.sidebar.page_link('pages/Your_Progress.py', label='Your Progress')
st.sidebar.page_link('pages/Keeping_Track.py', label='Keeping Track')
st.sidebar.page_link('pages/Meeting_Room.py', label='Meeting Room')

if st.sidebar.button("Log Out"):
    log_out()  # Call the log_out function when the button is clicked 
cathy_line =''
jim_line = ''
starting_line = ''
def get_response(jim_line):
    output =  "dummy"
    return output 
                                                                                                                                                                                                               
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["General", "Module 1", "Module 2", "Module 3", "Module 4", "Module 5", "Module 6", "Module 7", "Module 8"])
with tab1:
    pass
    # col01, col02 = st.columns([1, 2])
    # with col01:
    #     st.video("pages/game.mp4")
    # with col02:
    #     st.write("Chào mừng bạn đến với trò chơi thú vị này với Trí tuệ nhân tạo sáng tạo. Chúng tôi sẽ có ba trò chơi để khám phá khả năng sáng tạo của bạn với GenAI. Trò chơi đầu tiên có tên là Y Tường Sang Tạo. Trong trò chơi này, bạn sẽ viết ý tưởng cho một yêu cầu. Ý tưởng sáng tạo nhất sẽ đạt điểm cao nhất. Trò chơi thứ hai có tên là Kết Chu Thanh Truyền. Bạn cho tôi hai từ không liên quan, tôi sẽ viết một truyện ngắn dựa trên đó. Câu chuyện độc đáo, sáng tạo nhất sẽ đạt điểm cao nhất. Trò chơi thứ ba có tên là Thu trí thông minh của AI. Trong trò chơi này, bạn sẽ cho tôi một câu hỏi mà tôi có thể trả lời sai. Bạn cần biết câu trả lời chính xác. Nếu bạn có thể bắt tôi trả lời sai thì bạn sẽ được điểm.")
    # #with st.form("my_form"):
    #     #jim_line = st.text_area("Write your question here","", height=70)
    #     #submitted = st.form_submit_button("Submit")
    # if "openai_model" not in st.session_state:
    #     st.session_state["openai_model"] = "gpt-4o"        
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []        
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])        
    # if prompt := st.chat_input("What is up?"):
    #     game_instruction = "Act as a judge in a game about creativity in AI. In the first game called YTUONGSANGTAO, you will judge an idea for a idea of buying a Christmas gift now for yourself in 10 years time. Evalaute the answer basing on its creativity measured by  Novelty is the extent to which an idea is new, surprising, or different from existing solutions. Usefulness is the degree to which an idea is relevant, effective, or beneficial for the future of a mid-age Vietnamese person settled in Norway. Feasibility is the degree to which an idea is realistic, practical, or achievable with a person income around 50000 to 70000 usd per year. In the second game called NOICHUTHANHTRUYEN, players provide two unrelated words and a theme, like penguin, astronaut and adventure story. You create a short scenario or explanation connecting the two words following the theme. The scenario should be less than 120 words. Three evaluation criteria for this game are 1. Rare word combination - the uncommon of the used words, the less likelihood the word combination is, the better score it has. 2. Creative story plot - the more uncommon, or suprised plot development, the better score it has. 3. Plot logic - the more logic the generated story is the better score it has.  Give a score out of 10 for each criteria dimension, and the overall average score for the game, and explain your choice with the evaluation criteria. The third game is called THUTHACHAI. Answer the questions that players enter. Ask the players if the generated answer is correct or not. If it is not the player will get 3 points. Track the scores of all people. We will summarize the game when I say to end the game. Do all answer in Vietnamese!"
    #     st.session_state.messages.append({"role": "system", "content": game_instruction})
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #     with st.chat_message("user"):
    #         st.markdown(prompt)
    #     with st.chat_message("assistant"):
    #         stream = client.chat.completions.create(
    #             model=st.session_state["openai_model"],
    #             messages=[
    #                 {"role": m["role"], "content": m["content"]}
    #                 for m in st.session_state.messages
    #             ],
    #             stream=True,
    #         )
    #         response = st.write_stream(stream)
    #         response2 = client.audio.speech.create(
    #             model="tts-1",
    #             voice="nova",
    #             input=response
    #         )
    #         response2.write_to_file("output1.mp3")
    #         with open("output1.mp3", "rb") as audio_file:
    #             st.audio(audio_file, format='audio/mp3')
    #     st.session_state.messages.append({"role": "assistant", "content": response})
with tab2:
    st.image("https://miro.medium.com/v2/resize:fit:720/format:webp/1*fiEXMWcFg328ztjZEWYlpg.jpeg", width=400)
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.button("Characterizing a software project",key="ex1",use_container_width=True) 
    with col2:
        st.button("Stakeholder analysis",key="ex2",use_container_width=True) 
    with col3: 
        st.button("Project management areas",key="ex3",use_container_width=True) 
    with col4: 
        st.button("SWOT analysis",key="ex4",use_container_width=True) 
    with st.expander("Submit your exercise here"):
        with st.form("my_form1"):
            jim_email= st.text_input("Email to receive feedback", "12345678@std.usn")
            jim_line = st.text_area("Write your exercise here","", height=200)
            submitted = st.form_submit_button("Submit")
with tab3:
    st.image("https://cdn-cnhfh.nitrocdn.com/jsHsUxJJAapjeJICfnGvtaAAOHZlckTe/assets/images/optimized/rev-dfbdbb8/e360-media.s3.amazonaws.com/2024/07/07160602/2290114_ProjectScopeManagementPMA-ControlScopeProcessPMP_070524.jpg", width=400)
    col5, col6, col7, col8 = st.columns(4)
    with col5: 
        st.button("Github project setting",key="ex5",use_container_width=True) 
    with col6:
        st.button("Project Layout",key="ex6",use_container_width=True) 
    with col7: 
        st.button("Project success criteria",key="ex7",use_container_width=True) 
    with col8: 
        st.button("Requirement Gathering and Analysis",key="ex8",use_container_width=True) 
    col9, col10 = st.columns(2)
    with col9: 
        st.button("Work Breakdown Structure (WBS)",key="ex9",use_container_width=True) 
    with col10:
        st.button("Scope validation",key="ex10",use_container_width=True) 
    with st.expander("Submit your exercise here"):
        with st.form("my_form2"):
            jim_email= st.text_input("Email to receive feedback", "12345678@std.usn")
            jim_line = st.text_area("Write your exercise here","", height=200)
            submitted = st.form_submit_button("Submit")
with tab4:
    st.image("https://images.squarespace-cdn.com/content/v1/56acc1138a65e2a286012c54/1587053683921-RPMQIPHXBQFOIZOXRTGD/time-management-1966396_1920.jpg", width=400)
    col11, col12, col13 = st.columns(3)
    with col11: 
        st.button("Network Diagram and Critical Path Analysis",key="ex11",use_container_width=True) 
    with col12:
        st.button("Gantt Chart",key="ex12",use_container_width=True) 
    with col13: 
        st.button("Time control",key="ex13",use_container_width=True) 
    with st.expander("Submit your exercise here"):
        with st.form("my_form3"):
            jim_email= st.text_input("Email to receive feedback", "12345678@std.usn")
            jim_line = st.text_area("Write your exercise here","", height=200)
            submitted = st.form_submit_button("Submit")
with tab5:
    st.image("https://cortouchmedia.com.ng/wp-content/uploads/2023/05/prototyping.png", width=400)
    col14, col15 = st.columns(2)
    with col14: 
        st.button("Low Fidelity Prototype",key="ex14",use_container_width=True) 
    with col15:
        st.button("Prototying with Figma",key="ex15",use_container_width=True) 
    with st.expander("Submit your exercise here"):
        with st.form("my_form4"):
            jim_email= st.text_input("Email to receive feedback", "12345678@std.usn")
            jim_line = st.text_area("Write your exercise here","", height=200)
            submitted = st.form_submit_button("Submit")
with tab6:
    st.image("https://scrumorg-website-prod.s3.amazonaws.com/drupal/inline-images/2023-09/scrum-framework-9.29.23.png", width=400)
    col16, col17 = st.columns(2)
    with col16: 
        st.button("Scrum Project Management",key="ex16",use_container_width=True) 
    with col17:
        st.button("Sprint execution and report",key="ex17",use_container_width=True) 
    with st.expander("Submit your exercise here"):
        with st.form("my_form5"):
            jim_email= st.text_input("Email to receive feedback", "12345678@std.usn")
            jim_line = st.text_area("Write your exercise here","", height=200)
            submitted = st.form_submit_button("Submit")
with tab7:
    st.image("https://www.intuition.com/wp-content/uploads/2023/07/Risk-Management-Process.png", width=400)
    col18, col19 = st.columns(2)
    with col18: 
        st.button("Risk Management Table",key="ex18",use_container_width=True) 
    with col19:
        st.button("Communication Management Table",key="ex19",use_container_width=True) 
    with st.expander("Submit your exercise here"):
        with st.form("my_form6"):
            jim_email= st.text_input("Email to receive feedback", "12345678@std.usn")
            jim_line = st.text_area("Write your exercise here","", height=200)
            submitted = st.form_submit_button("Submit")
with tab8:
    st.image("https://www.tatvasoft.com/outsourcing/wp-content/uploads/2022/11/difference-between-software-testing-vs-quality-assurance.jpg", width=400)
    col20, col21, col22 = st.columns(3)
    with col20: 
        st.button("Non-functional requirements",key="ex20",use_container_width=True) 
    with col21:
        st.button("Test plan",key="ex21",use_container_width=True) 
    with col22:
        st.button("Usability test",key="ex22",use_container_width=True) 
    with st.expander("Submit your exercise here"):
        with st.form("my_form7"):
            jim_email= st.text_input("Email to receive feedback", "12345678@std.usn")
            jim_line = st.text_area("Write your exercise here","", height=200)
            submitted = st.form_submit_button("Submit")
with tab9:
    st.image("https://business.adobe.com/blog/basics/media_1f189f1c2c3c424441541e86d7b8b729ad795f205.jpeg", width=400)
    col23, col24, col25 = st.columns(3)
    with col23: 
        st.button("Sprint planning meeting",key="ex23",use_container_width=True) 
    with col24:
        st.button("Sprint review meeting",key="ex24",use_container_width=True) 
    with col25:
        st.button("Retrospective meeting",key="ex25",use_container_width=True) 
    with st.expander("Submit your exercise here"):
        with st.form("my_form8"):
            jim_email= st.text_input("Email to receive feedback", "12345678@std.usn")
            jim_line = st.text_area("Write your exercise here","", height=200)
            submitted = st.form_submit_button("Submit")
