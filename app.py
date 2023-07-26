import streamlit as st
import pandas as pd
import gspread
import numpy as np
import random
from oauth2client.service_account import ServiceAccountCredentials
import datetime


def connect_to_google_sheet():
        scopes = ["https://spreadsheets.google.com/feeds"]
# 为特定的账户开设key，然后然后把账户给到谷歌sheet的访问权限中，通过key访问这个账户关联的sheet
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scopes)
#这个json就是key，授权给谷歌的表格
        client = gspread.authorize(credentials)
# 这一段就牛逼了，这一段那串乱码是目标谷歌sheet地址中间那一部分，用.来确定要访问的工作表
        sheet_A = client.open_by_key(
        "1Ij0AS1JWU5558CA3dbQPBnz4KnXAVsIAK4WKDv3DmnU").worksheet('随机表')
        sheet_B = client.open_by_key(
        "1Ij0AS1JWU5558CA3dbQPBnz4KnXAVsIAK4WKDv3DmnU").worksheet('随机数')

        return sheet_A,sheet_B



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
        risk_level = st.radio("请选择风险分层", ("高风险", "中风险"))
        sheet_A, sheet_B = connect_to_google_sheet()
        first_column = sheet_B.col_values(1)
        available_numbers = set(range(1, 501)) - set(map(int, first_column))
        # 提供一个单选下拉，让用户选择研究中心
        center = st.selectbox("请选择研究中心", ['广西医科大学第一附属医院',	
                                                '河池市第一人民医院',	
                                                '百色市人民医院',	
                                                '平果市人民医院',	
                                                '来宾市人民医院',
                                                '武鸣区中医医院',	
                                                '宾阳县人民医院',	
                                                '广安市人民医院',	
                                                '阆中市人民医院',
                                                '攀枝花市中心医院',	
                                                '通江县人民医院',	
                                                '达州市达川区人民医院',	
                                                '宣汉县人民医院',	
                                                '凉山州第一人民医院',
                                                '巴中市中心医院',	
                                                '南江县人民医院'])
        patient_id = st.text_input("请输入患者的住院号")

        
        group = np.nan
        random_number = np.nan
        if st.button("开始随机"):
            if risk_level == "高风险":
                 # 首先从1-500中排除first_column中已经存在的数字，然后在剩下的数字中随机抽取一个
                 random_number = random.choice(list(available_numbers))
                 group = np.nan
                 if random_number % 2 == 0:
                     group = "对照组"
                 else:
                     group = "试验组"
                 random_number = "ONDEX" + str(random_number)
        random_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()


        if st.button("确认随机结果"):
        
            sheet_A.append_row([random_time,center,patient_id, random_number,risk_level,group],1)       
                
                
                 
                 

                 

             

        


        # Display a dataframe with example data
        
        
    else:
        st.error("Invalid username or password")

