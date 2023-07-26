import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials



def connect_to_google_sheet():
        scopes = ["https://spreadsheets.google.com/feeds"]
# 为特定的账户开设key，然后然后把账户给到谷歌sheet的访问权限中，通过key访问这个账户关联的sheet
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scopes)
#这个json就是key，授权给谷歌的表格
        client = gspread.authorize(credentials)
# 这一段就牛逼了，这一段那串乱码是目标谷歌sheet地址中间那一部分，用.来确定要访问的工作表
        sheet_A = client.open_by_key(
        "1Ij0AS1JWU5558CA3dbQPBnz4KnXAVsIAK4WKDv3DmnU").sheet1

        return sheet_A



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
        # Display a data interface after successful login
        st.header("随机系统")
        # Display a dataframe with example data
        
        df = pd.DataFrame({"Column1": ["Value1", "Value2"], "Column2": ["Value3", "Value4"]})
        st.dataframe(df)
    else:
        st.error("Invalid username or password")

