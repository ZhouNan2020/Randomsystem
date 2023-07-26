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
sheet_A, sheet_B = connect_to_google_sheet()

global center
global patient_id
global risk_level
risk_level = None


center = None
patient_id = None

    
        
# Display a data interface after successful login
st.markdown("# ONDEX研究随机系统", unsafe_allow_html=True)

risk_level = st.radio("请选择风险分层", ("高风险", "中风险"), key='risk_level')

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
                                        '南江县人民医院'], key='center')
patient_id = st.text_input("请输入患者的住院号", key='patient_id')


random_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()


def random_selection(risk_level, available_numbers):
    if risk_level == "高风险":
        random_number = random.choice(list(available_numbers))
        if random_number % 2 == 0:
            group = "对照组"
        else:
            group = "试验组"
        
    elif risk_level == "中风险":
        random_number = random.choice(list(available_numbers))
        if random_number % 2 == 0:
            group = "对照组"
        else:
            group = "试验组"
        
    # 将已经随机过的数字append到sheet_B的第一列的尾行
    sheet_B.append_rows([[random_number]], value_input_option='RAW')
    random_number = "ONDEX" + str(random_number)
    return random_number, group

random_results = []

if st.button("开始随机"):
    st.spinner(text="In progress...")

    random_number, group = random_selection(risk_level, available_numbers)
    random_results.append([random_time, center, patient_id, random_number, risk_level, group])
    dfrandom_results = pd.DataFrame(random_results, columns=['random_time', 'center', 'patient_id', 'random_number', 'risk_level', 'group'])
    dfrandom_results.columns = ["随机时间", "中心名称", "患者唯一识别码","随机号" ,"风险分层", "分组"]

    st.dataframe(dfrandom_results)
    sheet_A.append_rows([[random_time, center, patient_id, random_number, risk_level, group]], value_input_option='RAW')
    

st.markdown('[查看随机历史](https://randomsystem.streamlit.app/)')



