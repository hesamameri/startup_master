import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages
import time
import uuid

def sidebar_nav(disabeled):
    hide_pages(["Chatbot", "All_Tasks", "Chatbot_1", "Chatbot_2", "Chatbot_3", "Feedback", "Task_Information"])

    with st.sidebar:
        st.page_link("Chatbot.py", label="Home")
        st.write("Your tasks")
        with st.expander("Task 1", expanded=True):
            if(disabeled):
                st.page_link("pages/6_Task_Information.py", label="Your history progress", disabled=True, help="Submit form to unlock")
                st.page_link("pages/3_Chatbot_1.py", label="GPT Buddy", disabled=True, help="Submit form to unlock")
                st.page_link("pages/5_Feedback.py", label="Feedback", disabled=True, help="Submit form to unlock")
            
            else:
                st.page_link("pages/6_Task_Information.py", label="Your history progress")
                st.page_link("pages/3_Chatbot_1.py", label="GPT Buddy")
                st.page_link("pages/5_Feedback.py", label="Feedback")


def sticky_header(prev_text, current_text, next_text):
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
    header = st.container()
    if(current_text != "Feedback"):
        if(current_text == "Task Information"):
            header.info('Please read the task carefully to make sure you know how to communicate with ChatGPT in the next step')
        else:
            header.warning('Please note that the conversations will be saved and used in our master thesis. Do not include personal or sensitive information')
    header.header(current_text)
    col1, col2 = header.columns([1,1])
    with col1:
        if(prev_text != "None"):
            if st.button("Previous step: "+prev_text, type="secondary"):
                switch_page(prev_text.lower())
        else:
            if st.button("Previous step: "+prev_text, type="primary", disabled=True):
                switch_page(current_text.lower())
        
    with col2:
        if(next_text != "None"):
            if st.button("Next step: "+next_text, type="primary"):
                switch_page(next_text.lower())
        else:
            if st.button("Next step: "+next_text, type="primary", disabled=True):
                switch_page(current_text.lower())
            

    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)



# def demographic_form():
#     with st.form("my_form"):

#         st.selectbox(label="Stage", options=["early stage","...","3"])
#         st.text_input("Domain", placeholder="Tech, Health, etc...")
#         st.text_input("Location")
#         st.number_input("Year of business", value=None, placeholder=0)
#         st.selectbox(label="Year of business", options=["0-1 year","2-5 years","5-10 years", "10+ years"], placeholder="Choose an option",)
#         st.number_input("Size of business", value=None, placeholder=0)
      
#         # Every form must have a submit button.
#         submitted = st.form_submit_button("Submit")
#         if submitted:
#             return submitted
        

def demographic_form():
    with st.form("my_form"):
        st.write("To help us improve the research, please fill in the following information:")
        st.caption("Business details")
        st.selectbox("Stage", options=["Early stage", "Growth stage", "Mature stage"], placeholder="Select an option", index=None)
        st.selectbox("Year of business", ["<1 year", "2-5 years", "5-10 years", ">10 years"], placeholder="Select an option", index=None)
        st.number_input("Size of business", placeholder="Number of employees", value=None)
        st.text_input("Industry Sector", placeholder="Technology, healthcare, finance, etc.")
        st.selectbox("Revenue Range", ["No revenue", "<1M NOK", "1M-10M NOK", ">10M NOK"], placeholder="Select an option", index=None) #???
        st.text_input("Location", placeholder="City, Country")

        st.caption("Personal details")
        st.text_input("Company Role", placeholder="CEO, CTO, backend developer, UI/UX designer, etc.")
        st.selectbox("Level of experience with ChatGPT", ["No experience", "Some experience", "Very familiar"], placeholder="Select an option", index=None)  # FIX
       
        
        button_container = st.empty()
       # submitted = st.form_submit_button("Submit and consent to data usage as described on this page")
        #if submitted:
           # st.toast("Thank you for submitting. You can still update the information and submit again")
        

        button_container = st.empty()

        if st.session_state['user_id'] is not None:
            # User has already given consent
            if button_container.form_submit_button("Click to update form information"):
                st.toast("Thank you for submitting. You can still update the information and submit again")
        else:
            # User has not given consent yet
            if button_container.form_submit_button("Submit and consent to data usage as described on this page"):
                st.session_state['user_id'] = str(uuid.uuid4())
                button_container.form_submit_button('Click to update form information')
                st.toast("Thank you for submitting. You can still update the information and submit again")
