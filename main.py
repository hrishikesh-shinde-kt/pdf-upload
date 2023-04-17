import streamlit as st
import pandas as pd
import requests

# Displays table(s) according to the response.
def change_name_format(name):
  return name.replace("_", " ").title()

def get_column_name(keys):
  return [change_name_format(key) for key in keys.keys()]

def show_table(response):
  response_item = response['response']['data']
  for item in response_item:
    if isinstance(response_item[item], dict):
      df = pd.DataFrame(
        [list(response_item[item].values())],
        columns = get_column_name(response_item[item])
      )
    else: 
      df = pd.DataFrame(
        [list(i.values()) for i in response_item[item]],
        columns = get_column_name(response_item[item][0])
      )
    st.title(change_name_format(item))
    hide_table_row_index = """
            <style>
              thead tr th:first-child {display:none}
              tbody th {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(df)

#Getting pdf input
uploaded_pdf = st.file_uploader("Upload your pdf")
if uploaded_pdf is not None:
  url = "https://pivot-port-poldoc-health.attributum.com/api/ml_process"
  files = {
    "input_file" : uploaded_pdf
  } 
  data = {
    "insurance_company" : "star health",
    "data_type" : "Generic"
  }
  headers = {"Authorization": st.secrets["auth_key"]}

  #Post API call.
  response = requests.post(url, files=files, data=data, headers=headers)

  if response:
    show_table(response.json())

