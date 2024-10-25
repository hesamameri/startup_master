import streamlit as st
from st_pages import add_indentation, hide_pages,show_pages_from_config
import extra_streamlit_components as stx
import time
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(layout="wide") 

# show_pages_from_config()
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./styles.css")

add_indentation()
hide_pages(["All_Tasks","Chatbot_1", "Chatbot_2", "Feedback", "Task_Information"])



@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookie_manager.get_all()
with st.spinner('Loading page'):
    time.sleep(2)

# Fetch a specific cookie
user_consent_cookie = cookie_manager.get(cookie="userid")
print(user_consent_cookie, "hello")
#### SIDEBAR ####
with st.sidebar:
    st.write("Your tasks")
    with st.expander("Task 1", expanded=True):
        if user_consent_cookie:
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

        else:
            task_info = f"""
            <a href="Task_Information" target = "_self">
            <button type="button" class="not_clicked">
                Task information
            </button></a>
                """
            st.markdown(task_info, unsafe_allow_html=True)

            c1 = f"""
            <a href="Chatbot_1" target = "_self">
            <button type="button" class="disabeled" disabled>
                Chatbot 1
            </button></a>
                """
            st.markdown(c1, unsafe_allow_html=True)

            c2 = f"""
            <a href="Chatbot_2" target = "_self">
            <button type="button" class="disabeled" disabled>
                Chatbot 2
            </button></a>
                """
            st.markdown(c2, unsafe_allow_html=True)

            feedback = f"""
            <a href="Feedback" target = "_self">
            <button type="button" class="disabeled" disabled>
                Feedback
            </button></a>
                """
            st.markdown(feedback, unsafe_allow_html=True)


#### MAIN CONTENT ####

st.header("All tasks")
st.write("Here is a list of all the tasks created for this study. To start the study go to one of the tasks")

st.subheader("Task 1: Task name")
if st.button("Go to task", "t1"):
    switch_page("task information")
st.write("Task description")

st.subheader("Task 2: Task name")
if st.button("Go to task", "t2"):
    switch_page("task information")
st.write("Task description")
