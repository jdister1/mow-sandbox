import streamlit as st
import pandas as pd
import boto3
from io import BytesIO

session = boto3.Session(
    aws_access_key_id=st.secrets["aws"]["access_key"],
    aws_secret_access_key=st.secrets["aws"]["secret_access_key"]
)
s3 = session.client('s3')
bucket_name = 'mow-dashboard'
file_key = 'WSMOW Food Costs for 2024.xlsx'
excel_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
body = excel_obj['Body'].read()
df = pd.read_excel(BytesIO(body), engine='openpyxl', skiprows=7)
print(df.columns.tolist())
cost_df = df[['Month','per Meal ', 'per Meal','per Meal.2','per Meal.3']].dropna()
cost_df.columns = ['Month', 'Per Meal_rrlwd','Running Avg_rrlwd', "Per Meal_fv","Running Avg_fv"]
#rr_df.style.format({'Cost Per Meal': '${:,.2f}'})
#rr_df.style.format({'Running Average': '${:,.2f}'})

cost_df = cost_df[~cost_df['Month'].str.contains('Oct-Dec|Jan-Dec', na=False)]
st.sidebar.write("Westshore MOW")
st.write("Food Cost")
st.line_chart(
    cost_df,
    x="Month",
    y=["Per Meal_rrlwd","Running Avg_rrlwd","Per Meal_fv","Running Avg_fv"],
    color=["#da413c", "#ff91af", "#0390bc","#fbd266"]
)
