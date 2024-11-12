import streamlit as st
import os
#from decouple import config
import openai
import streamlit as st
#from streamlit_chat import message
from email.policy import default
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import openai
from datetime import datetime
import pymongo
import json


st.set_page_config(layout = "wide", page_title="StartupGPT")
from auth import log_out
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


#import chatbot_utils as cu
st.sidebar.page_link('pages/Project_Buddy.py', label='Project Buddy')
st.sidebar.page_link('pages/Your_Progress.py', label='Your Progress')
st.sidebar.page_link('pages/Customer_Meeting.py', label='Customer Meeting')
if st.sidebar.button("Log Out"):
    log_out()  # Call the log_out function when the button is clicked
cathy_line =''
jim_line = ''
starting_line = "Let's roleplay. Act as a project owner who will convert three lab rooms at USN Bø campus into a co-working space named USNStart at Bø campus, the main building. The coworking space is in a planning phase and will be open by the end of the year. You will get 3 rooms in an area of 500 square meters together. It will include: Open Workspace: This is the heart of a coworking space, featuring flexible seating arrangements with communal desks, tables, and chairs. It's suitable for individual work, informal meetings, and collaborative projects. There is space for 60 individual working here. Private offices: Small, fully-furnished offices that can accommodate individuals or small teams, offering more privacy and a dedicated workspace. The total capacity is 6 private offices. Meeting rooms: Various-sized meeting rooms equipped with projectors and whiteboards for presentations, client meetings, or team discussions. There are 5 meeting rooms in total. Lounge Area: Comfortable seating areas, often with sofas and coffee tables, providing a relaxed atmosphere for informal meetings or relaxation. Kitchen and Dining Area: A well-equipped kitchen or kitchenette with facilities for preparing meals and dining. It also offers complimentary coffee, tea, and snacks. Printing and Scanning area: Equipment for printing, scanning, and photocopying documents. Game room: A recreational space with games like billiards, ping-pong, or video games, encouraging breaks and social interaction. There are also plenty of parking places. As of today, the tenants are Revisorteam, YourCompanion, GreenEnergy, and VismaAI, who sit in private offices. We want to attract students who want to work and become entrepreneurs. We also want to attract individuals who work in groups—larger companies centrally in our cities, who live in the region and/or want to move to the region, and in that way, take their work home and then be able to sit in a co-working building, where they meet other like-minded people and not alone in a home office. There are available offers for seating in the coworking space: Day Pass: Day passes allow members to access the coworking space for a single day. This costs 699 NOK per day. Monthly Membership: Monthly memberships grant unlimited access to the coworking space for a fixed monthly fee. This costs 6000 NOK per month. Student membership: the membership for students. This costs 9000 NOK per semester (6 months). Annual Fixed Desk: members may have their own desk within the enclosed office space, which offers more privacy and can accommodate small teams. This costs 50,000 NOK per year. Private Office Desk: In private offices, members may have their own desk within the enclosed office space, which offers more privacy and can accommodate small teams. This costs 20,000 NOK per month per office. I would like to create a landing page to increase our visibility and attract customers to us. We want to have: Clear and Engaging Headline: Start with a clear, attention-grabbing headline that communicates the core value of your coworking space. Compelling Visuals: Use high-quality images or videos of the coworking space, showcasing the interior, workstations, communal areas, and facilities. You come up with your own ideas about the interior design of the space. Membership Plans and Pricing: Display your membership options, pricing, and any special offers or discounts prominently. Include a call-to-action (CTA) button to encourage visitors to explore plans. Amenities and Facilities: List the key amenities and facilities available in your coworking space, such as high-speed internet, meeting rooms, coffee lounge, and more. Highlight what makes your space unique. Location Information: Clearly state your coworking space's location, including the address, a map, and information about nearby public transportation or parking options. Testimonials and Reviews: Include positive testimonials or reviews from current members. Real feedback can build trust and credibility. Contact Information: Provide multiple contact options, including an email address, phone number, and a contact form. Make it easy for potential members to get in touch. About Us Section: Share a brief overview of your coworking space's history, mission, and values. Highlight what makes your community unique. Responsive Design: Ensure that the landing page is responsive and mobile-friendly, so it displays correctly on all devices and screen sizes. Privacy and Security: Include a section about data privacy and security to reassure potential members that their information will be protected. Floor plan: showing the proposed floor plan and images of interior designs. Booking: allow people with day passes or monthly memberships to book available desks in the open workspace for the current month. A floor map should be displayed, and desk selection should be interactive and visual on the map. A member can only choose to book one desk for one day at a time. A confirmation should be displayed after the reservation is done. Project Brief: USNStart Coworking Space Website. The primary objective of this project is to create a dynamic and engaging website for USNStart Coworking Space, located at the Bø campus of the University of South-Eastern Norway (USN). The website should serve as an informative, user-friendly, and visually appealing platform to attract potential members, provide information about our coworking space, and facilitate desk booking for members. The website should implement all requirements described above. The scope of the project encompasses the design, development, and launch of the USNStart Coworking Space website. This includes, but is not limited to: Development of a responsive website accessible on desktop, tablet, and mobile devices. Design and layout of the website, considering the provided interior design concepts and floor plan. Creation of pages and content that convey key information about the coworking space, membership plans, and existing tenants. Inclusion of images, videos, and visuals to showcase the interior and amenities. Integration of privacy and security measures to protect user data. Coordination with project stakeholders for feedback and review. We are very flexible with design ideas. For website design inspiration see: https://meshcommunity.com/hubs/digs/ https://www.wework.com/l/coworking-space/oslo https://www.spacesworks.com/nb/oslo-nb/kvadraturen/ We are also flexible with the floor map ideas. For inspiration, see: https://pin.it/3sLJ0EQ https://pin.it/43gdiRI https://workdesign.com/wp-content/uploads/2012/11/Coworking-Concept-Floor-Plan-720x405.jpg The desk reservation function is in a very early stage. We want your proposal, both about the process of booking and the user experience of the booking process. We do not have any brand design yet. You are all free to design the logo, color palette, typography, and icons. Technically, we want prototypes to be made with Figma. The prototypes should be interactive with multiple screens. The final website should be implemented using HTML, CSS, and JavaScript. Any supporting tool to generate the code is allowed, for instance, siter.io, or chatgpt. The website can be static, without the backend. Implementation of the backend part is a plus. In the end, the website should be hosted and published (just for the purpose of this course). It is NOT allowed to use any Content Management Systems (WordPress, Webflow, etc.). The code should be written or generated from scratch. We can ignore other aspects of web publication, such as Web analytics, SEO, and interoperability. In order to test the landing page, I would like to run a usability test with some students on campus for the landing page and the booking function. The project will start from the second week of January 2024 and end at the end of April 2024. The success of the USNStart Coworking Space website project can be evaluated based on various criteria. Success in this context can be measured in terms of meeting project objectives, delivering value to the target audience, and achieving the desired outcomes. Here are the criteria of success for this project: Alignment with Project Objectives: The website effectively aligns with the project objectives as defined in the project brief, including creating an engaging online presence for the coworking space and facilitating desk bookings. Fulfillment of all user stories: all stated user stories should be documented, analyzed, prototyped, implemented, and tested. Quality of the visual elements: the visual elements should be comparable to the given examples. Quality and scope of codebase: the codebase should be at a reasonable size for a team of four developers working in a month. Usability test: The website should meet or exceed the expectations of its target audience, in this case, to test with students. Demonstration of Agile team: the team should work and follow Agile practices. Teamwork: the extent that teams frequently meet, and team maturity demonstrated via the evolution of the type of team issues over time. Quality of document: the project report should be written clearly with a reasonable reading flow, logical organization of sections, avoidance of jargon, and use of language appropriate for the target audience. Proper format a document with page numbers, captions for tables, figures, explanations for abbreviations, high resolution for included figures, and a reference section. Students may need to ask questions, seek clarifications, or provide progress updates during the development process. Communication should be done via email. Each email should have a title - PRO1000 - Group number - Main points to communicate. Emails should be sent to angu@usn.no. Please use this persona to provide feedback and guidance to students to collect requirements, clarify student concerns, answer their questions, and guide them to develop and evaluate the landing page. Now wait for students' questions. Try to be as detailed as possible. If the questions from students are not clear enough to give them a detailed answer, then ask them to clarify or give more details in their questions. For each question, try to define and explain a concept or term if the student introduces them in their questions. Try to answer questions in paragraphs; if using bullet."

def get_response(jim_line):
    output =  "dummy"
    return output 
                                                                                                                           
openai.api_key = st.secrets["api"]["key"]

tab1, tab2 = st.tabs(["Interactive Tutor", "Step-by-step Guideline"])

# Interactive Tutor Tab
with tab1:
    st.title("🏢 Interactive Tutor")
    st.markdown("""
        Ask for explanation and examples by inputting a prompt.
    """, unsafe_allow_html=True)

    with st.form("my_form"):
        jim_line = st.text_area("Write your command here:", "", height=10, key='option')
        submitted = st.form_submit_button("Submit")

    if submitted and jim_line:
        # Call GPT-4 API on form submission
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": jim_line}
            ]
        )
        st.write("Response from GPT-4:")
        st.write(response.choices[0].message.content)  # Output the response from GPT-4

# Step-by-step Guideline Tab
with tab2:
    st.title("🏢 Step-by-step Guideline")
    st.markdown("""
    Have you done with:  
        1. Project planning 
        2. WBS 
        3. Gantt Chart 
        4. Project implementation 
        5. Requirement description 
        6. Team and role assignment 
        7. Prototyping  
        8. Github and project configuration  
        9. Meetings 
        10. Testing
    """)



# openai.api_key = st.secrets["api"]["key"]

# tab1, tab2 = st.tabs(["Interactive Tutor", "Step-by-step Guideline"])

# # Function to save data to JSON file
# def save_to_json(user_input, api_response):
#     data = {
#         "user_input": user_input,
#         "api_response": api_response
#     }
    
#     # Load existing data from the JSON file if it exists
#     try:
#         with open("responses.json", "r") as f:
#             all_data = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         all_data = []

#     # Append new data to the list
#     all_data.append(data)

#     # Save the updated list back to the JSON file
#     with open("responses.json", "w") as f:
#         json.dump(all_data, f, indent=4)

# # Function to load conversation history
# def load_conversation():
#     try:
#         with open("responses.json", "r") as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# # Interactive Tutor Tab
# with tab1:
#     st.title("🏢 Interactive Tutor")
#     st.markdown("""
#         Ask for explanation and examples by inputting a prompt.
#     """, unsafe_allow_html=True)

#     # Load the previous conversation history
#     conversation_history = load_conversation()

#     # Display only the most recent interaction (if any)
#     if conversation_history:
#         # Show the last interaction
#         last_entry = conversation_history[-1]
#         st.markdown(f"**User:** {last_entry['user_input']}")
#         st.markdown(f"**GPT-4:** {last_entry['api_response']}")
#         st.markdown("---")  # Separator for clarity

#     # Input form for new message
#     with st.form("my_form", clear_on_submit=True):
#         jim_line = st.text_area("Write your command here:", "", height=10, key='option')  # Unique key for the form input
#         submitted = st.form_submit_button("Submit")

#     if submitted and jim_line:
#         # Call GPT-4 API on form submission
#         response = openai.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": jim_line}
#             ]
#         )
#         api_response = response.choices[0].message.content
        
#         # Save user input and API response to JSON
#         save_to_json(jim_line, api_response)

#         # Display the new message
#         st.markdown(f"**User:** {jim_line}")
#         st.markdown(f"**GPT-4:** {api_response}")
#         st.markdown("---")

#     # Ensure the input box always stays at the bottom with a unique key
 

# # Step-by-step Guideline Tab
# with tab2:
#     st.title("🏢 Step-by-step Guideline")
#     st.markdown("""
#     Have you done with:  
#         1. Project planning 
#         2. WBS 
#         3. Gantt Chart 
#         4. Project implementation 
#         5. Requirement description 
#         6. Team and role assignment 
#         7. Prototyping  
#         8. Github and project configuration  
#         9. Meetings 
#         10. Testing
#     """)