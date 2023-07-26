import streamlit as st
import webbrowser


# Define a function to verify the user's credentials
def verify_credentials(username, password):
    # Here you should implement the logic to verify the user's credentials
    # For simplicity, we will just check if the username is "admin" and the password is "password"
    if username in ["test",'test1'] and password in ["000",'111']:
        return True
    else:
        return False

# Create a form for the user to enter their credentials
with st.form(key='login_form'):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button(label='Login')

# If the user clicks the login button, verify their credentials
if submit_button:
    if verify_credentials(username, password):
        st.success("Login successful")
        # Automatically redirect to the specified URL
        
        webbrowser.open_new_tab("https://randomsystem.streamlit.app/")


        