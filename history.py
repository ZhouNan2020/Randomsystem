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
        
        return sheet_A


sheet_A = connect_to_google_sheet()
data = sheet_A.get_all_records()
df = pd.DataFrame(data)
df.columns = ["随机时间", "中心名称", "患者唯一识别码","随机号" ,"风险分层", "分组"]

# Convert the '患者唯一识别码' column to numeric, errors set to 'coerce' will replace non numeric to NaN
df['患者唯一识别码'] = pd.to_numeric(df['患者唯一识别码'], errors='coerce')

st.dataframe(df)
# 提供下载st.download_button,使用户可以下载df到本地任意路径，文件名为"随机表.csv"
df.to_excel('随机表.xlsx', index=False)
st.download_button(label="Download Excel file", data=pd.read_excel('随机表.xlsx').to_csv(index=False), file_name='随机表.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')




