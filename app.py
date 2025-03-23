import streamlit as st

# Define a function for the login page
def login_page():
    st.title("Login")
    st.subheader("Movie Recommendation System")
    st.write("\n")  # Add space 

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
      
    st.write("\n")  # Add space 

    # Check if the login button is pressed
    if st.button("Login", key="login_button", use_container_width=True, on_click=None, args=None, kwargs=None):
            # Check if the user exists in session state
            if 'users' in st.session_state and username in st.session_state.users:
                # Authenticate user
                if st.session_state.users[username] == password:
                    st.success("Login successful!")
                    st.session_state.logged_in = True  # Set a session variable for logged-in status
                    st.session_state.current_user = username  # Store the username of the logged-in user
                    st.rerun()  # Refresh the page to load the main app after successful login
                else:
                    st.error("Invalid password. Please try again.")
            else:
                st.error("Username does not exist. Please sign up first.")

    st.divider()
    st.text(f"Doesn't have an account?")

    # Sign Up button that takes the user to the sign-up page
    if st.button("Sign Up", use_container_width=True, on_click=None, args=None, kwargs=None):
            st.session_state.page = "Sign Up"
            st.rerun()  # Refresh the page to show the sign-up form

# Define a function for the sign-up page
def signup_page():
    st.title("Create Account for Movie Recommendation System")
    
    # Input fields for creating a new username and password
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    
    st.write("\n")  # Add space 
    col1, space, col3 = st.columns([4, 10, 2])  # Adjust the column widths as needed

    # Check if the signup button is pressed
    with col3:
        if st.button("Sign Up"):
            if new_username in st.session_state.get('users', {}):
                st.error("Username already exists. Please choose another one.")
            elif new_username and new_password:
                # Save the new user credentials in session state
                if 'users' not in st.session_state:
                    st.session_state['users'] = {}  # Initialize the users dictionary
                st.session_state.users[new_username] = new_password
                st.success("Sign up successful! You can now log in.")
                st.session_state.signup_successful = True  # Set a flag to show a success message
                st.session_state.page = "Login"  # Redirect back to login page
                st.rerun()  # Refresh the page to go to the login page after successful signup
            else:
                st.error("Please fill in both fields.")

    # Back button that takes the user back to the login page
    with col1:
        if st.button("Back to Login"):
            st.session_state.page = "Login"
            st.rerun()  # Refresh the page to show the login form

def logout():
    # Clear only the login-related session state (keep the user data intact)
    st.session_state.logged_in = False
    st.session_state.current_user = None  # Clear the current user information
    st.session_state.page = "Login"  # Redirect to login page
    st.rerun()  # Refresh the page to show login screen

# Main app logic
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    if 'page' not in st.session_state or st.session_state.page == "Login":
        login_page()  # Show the login page by default
    elif st.session_state.page == "Sign Up":
        signup_page()  # Show the sign-up page when the user clicks the "Sign Up" button
else:
    # Once logged in, show the main app (existing pages and navigation)
    st.markdown("""
        <style>
            div[data-testid="stSidebarNav"] ul {
                font-size: 17px !important;  
            }
                
            div[data-testid="stSidebarNav"] ul li {
                padding: 2px 2px !important;  
            }
            div[data-testid="stSidebarNav"] ul li:hover, 
            div[data-testid="stSidebarNav"] ul li:active {
                box-shadow: 0 0 5px #FF4B4B !important;  
                transition: box-shadow 0.4s ease-in-out
            }
        </style>
    """, unsafe_allow_html=True)

    project_page_1 = st.Page(
        "pages/movie_recommend_page.py",
        title="Movie Recommendation",
        icon=":material/movie:",
        default=True,
    )
    project_page_2 = st.Page(    
        "pages/emotion_based_page.py",
        title="Emotion-Based Recommendation",
        icon=":material/mood:",
    )
    user_page = st.Page(    
        "pages/user.py",
        title="User profile",
        icon=":material/account_circle:",
    )
    pg = st.navigation(
        {
            "Movie Recommendation System": [project_page_1, project_page_2],
            "User": [user_page, logout],
        }
    )

    pg.run()