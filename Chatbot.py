
import streamlit as st
st.set_page_config(layout="wide", page_title="ProjectGPT")

import uuid
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi 
from streamlit_js_eval import streamlit_js_eval
from chatbot_utils import check_user_login, gather_feedback, local_css, init_connection



#-------------------------------------Style Settings------------------------------------------------


local_css("./styles.css")

#------------------------------------------USER Authentication-------------------------------------------
check_user_login()
    



#------------------------------------------DATABASE CONNECTION-------------------------------------------
client = init_connection()

#------------------------------------------PAGE LAYOUT----------------------------------------------------
st.title("Welcome to ProjectGPT")

def display_form():
    # """Displays the form for both new and returning users."""
    st.subheader("Log In")
    #st.caption("Personal details")
    st.session_state['username'] = st.text_input("Enter your username", value=st.session_state.get('username', ''), placeholder="Group12_2025")
    st.session_state['password'] = st.text_input("Enter your password", value=st.session_state.get('password', ''), placeholder="mypassword", )
    #st.write("By submitting the form you are consenting to:")
    #lst3= [
    #    "having received and understood information about the project", 
    #    "the participation in this research, including communicating with chatbots and answering the questionnaire", 
    #    "the collection of your data as described in on this page",
    #    "having had the opportunity to ask questions"
    #]
    #s = ''
    #for i in lst3:
    #    s += "- " + i + "\n"
    #st.markdown(s) 
    

    #st.caption("Business details (Information regarding business details will be used as context by the chatbots)")
    #stage_options = [
    #    "Seed Stage: Small team working on the development of a business plan and product, with minimal or personal funding", 
    #    "Early Stage: Product is introduced to the market, continued innovation is necessary, focus on building a customer base", 
    #    "Growth Stage: Established presence in the market and a steady customer base, focus on increasing revenue and market share", 
    #    "Expansion Stage: Well-established and financially stable, focus on maintaining market position and exploring new opportunities"
    #]
    #year_options = [
    #    "<1 year", 
    #    "1-5 years", 
    #    "5-10 years", 
    #    ">10 years"
    #]
    #gpt_exp_options = [
    #    "No experience: I have never used ChatGPT or have only tried it once or twice", 
    #    "Beginner: I have used ChatGPT a few times, but I'm still learning the basics", 
    #    "Intermediate: I use ChatGPT regularly and am familiar with many of its features", 
    #    "Experienced: I have extensive experience with ChatGPT and use it proficiently for various tasks", 
    #    "Advanced: I deeply understand ChatGPTs capabilities and limitations, and have possibly used it in professional or advanced projects"
    #]
   
    # https://www.ilo.org/global/industries-and-sectors/lang--en/index.htm
    # industry = ["Agriculture; plantations;other rural sectors" ,"Basic Metal Production" ,"Chemical industries" ,"Commerce", "Construction", "Education", "Financial services; professional services", "Food; drink; tobacco", "Forestry; wood; pulp and paper", "Health services", "Hotels; tourism; catering", "Mining (coal; other mining)", "Mechanical and electrical engineering", "Media; culture; graphical", "Oil and gas production; oil refining", "Postal and telecommunications services", "Public service", "Shipping; ports; fisheries; inland waterways", "Textiles; clothing; leather; footwear", "Transport (including civil aviation; railways; road transport", "Transport equipment manufacturing","Utilities (water; gas; electricity)"] 
   
    # https://www.ssb.no/en/klass/klassifikasjoner/6 
    #industry = [
    #    "Accommodation and Food Service Activities",
    #    "Administrative and Support Service Activities",
    #    "Agriculture, Forestry and Fishing",
    #    "Arts, Entertainment and Recreation",
    #    "Construction",
    #    "Education",
    #    "Electricity, Gas, Steam and Air Conditioning Supply",
    #    "Financial and Insurance Activities",
    #    "Human Health and Social Work Activities",
    #    "Information and Communication",
    #    "Manufacturing",
    #    "Mining and Quarrying",
    #    "Professional, Scientific and Technical Activities",
    #    "Public Administration and Defence; Compulsory Social Security",
    #    "Real Estate Activities",
    #    "Transportation and Storage",
    #    "Water Supply; Sewerage, Waste Management and Remediation Activities",
    #    "Wholesale and Retail Trade; Repair of Motor Vehicles and Motorcycles",
    #    "Other"
    #]
    #st.session_state['stage'] = st.selectbox("Stage", options=stage_options, index=get_selectbox_index(stage_options, 'stage'), placeholder="Select an option")
    #st.session_state['year'] = st.selectbox("Year of business", year_options, index=get_selectbox_index(year_options, 'year'), placeholder="Select an option")
    #st.session_state['size'] = st.number_input("Size of business", step=1, min_value=0, value=st.session_state.get('size'), placeholder="Number of employees", )
    #st.session_state['industry'] = st.text_input("Industry", value=st.session_state.get('industry', ''), placeholder="Technology, healthcare, finance, etc.")
    #st.session_state['industry'] = st.selectbox("Industry", industry, index=get_selectbox_index(industry, 'industry'), placeholder="Select an option")
    # Uncomment the following line if needed
    # st.session_state['revenue'] = st.selectbox("Revenue Range", ["No revenue", "<1M NOK", "1M-10M NOK", ">10M NOK"], placeholder="Select an option") 
    #st.session_state['location'] = st.text_input("Location", value=st.session_state.get('location', ''), placeholder="City, Country")

    
    #st.session_state['gpt_experience'] = st.selectbox("Level of experience with ChatGPT", gpt_exp_options, index=get_selectbox_index(gpt_exp_options, 'gpt_experience'), placeholder="Select an option")




def write_data(mydict):
    db = client.usertests #establish connection to the 'test_db' db
    backup_db = client.usertests_backup
    items = db.cycle_3 # return all result from the 'test_chats' collection
    items_backup = backup_db.cycle_3
    items.insert_one(mydict)
    items_backup.insert_one(mydict)

def get_user_feedback(feedback):
    user_feedback = {"Task-1":{"id": st.session_state['user_id'], "time": datetime.now(), "Chatbot_versions": "C1: dem+rag, C2: dem, C3: dem+prompt+rag", "Demographic": feedback}}
    return user_feedback

def update_chat_db(feedback):
    db = client.usertests 
    backup_db = client.usertests_backup
    user_feedback = get_user_feedback(feedback)

    print("form:", user_feedback)
    print("userid:", st.session_state['user_id'])

    print(len(list(db.cycle_3.find({"Task-1.id": st.session_state['user_id']}))))

    if len(list(db.cycle_3.find({"Task-1.id": st.session_state['user_id']}))) > 0:
        print("opdaterte chatobjekt")
        db.cycle_3.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Demographic": feedback}})
        backup_db.cycle_3.update_one({"Task-1.id": st.session_state['user_id']}, {"$set": {"Task-1.time": datetime.now(), "Task-1.Demographic": feedback}})

    else:
        write_data(user_feedback)
        print("lagret ny chatobjekt")


def get_selectbox_index(option_list, session_state_key):
    # """Returns the index of the current session state value in the options list, or None if not found."""
    try:
        return option_list.index(st.session_state[session_state_key])
    except (ValueError, KeyError):
        return None  # Return None to use the placeholder



def handle_submit(is_new_user, submit_text):
    # """Handles the form submission for new and returning users."""
    if is_new_user:
        st.session_state['user_id'] = str(uuid.uuid4())

    st.toast("Thank you for submitting. You can still update the information and submit again")
    
    if submit_text != "Click to update form information":
        button_container.form_submit_button("Click to update form information")
        st.info("You can now access the tasks in the sidebar")
    all_feedback = gather_feedback()
    update_chat_db(all_feedback)

with st.form("test_form"):
    is_new_user = st.session_state.get('user_id') is None
    display_form()

    submit_text = "Log In" if is_new_user else "Click to update form information"
    button_container = st.empty()

    if button_container.form_submit_button(submit_text):
        handle_submit(is_new_user, submit_text)


st.subheader("Information about the project")
st.write("ProjectGPT is a prototype of a virtual assistant built on GPT technology. ProjectGPT will support students to learn from the courses")

st.subheader("Who is responsible for the research project?")
st.write("Department of Economic and Informatikk, Business School, University of South Eastern Norway")

st.subheader("Voluntary Participation")
st.write("Your participation in this study is entirely voluntary. You have the right to withdraw at any time without any negative consequences. If you wish to withdraw all the data obtained concerning you for this study is deleted immediately. You will not be able to recover your data after withdrawing. To withdraw from the study click the button below:")
withdraw_button_container = st.empty()

if st.session_state['user_id'] is None:
    withdraw_button_container.button("Click to withdraw from study", type="primary", disabled=True, help="You have not entered the study")
else:
    if withdraw_button_container.button("Click to withdraw from study", type="primary", disabled=False):
        
        print("witdrawn") ## Add modal when feature is released
        db = client.usertests
        backup_db = client.usertests_backup

        if len(list(db.cycle_3.find({"Task-1.id": st.session_state['user_id']}))) > 0:
            db.cycle_3.delete_one({"Task-1.id": st.session_state['user_id']})
            backup_db.cycle_3.delete_one({"Task-1.id": st.session_state['user_id']})

        for key in st.session_state.keys():
            del st.session_state[key]
        
        st.session_state['user_id'] = None  
        
        withdraw_button = withdraw_button_container.button("You have successfully withdrawn from the study. All data associated to you has been deleted", type="primary", disabled=True)   
        consent_button = button_container.form_submit_button('Submit and consent to data usage as described on this page')

        streamlit_js_eval(js_expressions="parent.window.location.reload()")


st.subheader("Confidentiality and Data Protection")
lst = [
    "We will only use your information for the purposes we have stated in this document.", 
    "All personal data collected during this study will be treated confidentially and in accordance with privacy regulations.", 
    "We will implement appropriate technical and organizational measures to ensure the security of your data.", 
    "Data will be anonymized", 
    "The data will be stored securely in a secure database and will only be accessible to the research team."
]
s = ''
for i in lst:
    s += "- " + i + "\n"
st.markdown(s)
st.subheader("What gives us the right to handle data about you?")
st.write("We process information about you based on your consent.")
st.write("On behalf of USN, Sikt – The Knowledge Sector's Service Provider (Kunnskapssektorens tjenesteleverandør in Norwegian) has assessed that the processing of personal data in this project is in accordance with the data protection regulations.")

####### SIDEBAR #######
# components.sidebar_nav(st.session_state['user_id'] is None)

