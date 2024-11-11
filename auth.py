import streamlit as st
import toml

def load_user_credentials():
    try:
        secrets = toml.load(".streamlit/secrets.toml")  # Assuming the secrets.toml file is in the same directory
        return secrets.get("users", {})
    except Exception as e:
        st.error(f"Failed to load credentials from secrets.toml: {e}")
        return {}

USER_CREDENTIALS = load_user_credentials()

# Initialize session state for necessary variables
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'password' not in st.session_state:
    st.session_state['password'] = ""
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'  # Default to login page if no page is set

def display_login_form():
    """Display the login form."""
    st.subheader("Log In")
    username = st.text_input("Username", value=st.session_state.get('username', ''))
    password = st.text_input("Password", type="password", value=st.session_state.get('password', ''))
    
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state['user_id'] = username
            st.session_state['is_logged_in'] = True
            st.session_state['username'] = username
            st.session_state['password'] = password
            st.session_state['page'] = 'terms'  # Move to terms page after successful login
        else:
            st.error("Invalid credentials. Please try again.")

def display_terms_of_agreement():
    """Display the terms of agreement page."""
    st.subheader("Terms of Agreement")
    st.write("""
        Please read the following terms of agreement carefully before proceeding with the study.
        - You agree to participate in the study.
        - Your data will be handled according to privacy policies.
    """)
    
    agree = st.checkbox("I Agree to the Terms and Conditions")
    
    if agree:
        st.session_state['page'] = 'main_page'  # Move to main app page after agreeing
    else:
        if st.button("Leave Study"):
            st.session_state['is_logged_in'] = False
            st.session_state['page'] = 'login'  # Reset to login page if user leaves

def display_app_page():
    """Display the main app page or one of the app pages after login."""
    st.title(f"Welcome {st.session_state['username']}")
    st.write("This is the main page of the application!")
    
    # Optionally display a sidebar if the user is logged in
    if st.session_state['is_logged_in']:
        with st.sidebar:
            st.header("Sidebar")
            st.write(f"User: {st.session_state['username']}")
            if st.button("Project Buddy"):
                st.session_state['page'] = 'Project Buddy'
            elif st.button("Your Progress"):
                st.session_state['page'] = 'Your Progress'
            elif st.button("Customer Meeting"):
                st.session_state['page'] = 'Customer Meeting'    
    
    # Content for the main app
    st.write("Main app content goes here.")
    
    # Provide navigation for users to go to other pages
    if st.button("Project Buddy"):
        st.session_state['page'] = 'Project Buddy'
    elif st.button("Your Progress"):
        st.session_state['page'] = 'Your Progress'
    elif st.button("Customer Meeting"):
        st.session_state['page'] = 'Customer Meeting'

# Main logic to decide what to show based on session state
if st.session_state['is_logged_in']:
    if st.session_state['page'] == 'terms':
        display_terms_of_agreement()
    elif st.session_state['page'] == 'main_page':
        display_app_page()
    
else:
    # Show the login page if not logged in
    display_login_form()


def log_out():
    st.session_state['user_id'] = None
    st.session_state['page'] = 'login'
    st.switch_page('Chatbot.py')