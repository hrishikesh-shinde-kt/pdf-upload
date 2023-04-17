import streamlit as st
import pandas as pd
import requests

st.set_page_config(
  page_title="PDF-Uploader",
  # page_icon=":computer:",
  layout="wide",  # sets page to wide mode as default. 
  # initial_sidebar_state="expanded"
)

# Adds logo and title on screen.
def add_logo():
  # Create a container for the logo and title
  header = st.container()

  # Add a logo to the left column
  with header:
    col1, col2 = st.columns(2)
    with col1:
      st.image('http://placekitten.com/200/200')

    with col2:
      st.title('PDF-Uploader')
  
  # st.image("http://placekitten.com/200/200", width=30)
  # st.write("# PDF-Uploader")

# Formats text.
def change_name_format(name):
  return name.replace("_", " ").title()

# Returns list of keys of a dictonary.
def get_column_name(keys):
  return [change_name_format(key) for key in keys.keys()]

# Displays table(s) according to the response.
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

# Main logic.
add_logo()

#Getting Policy type input.
option = st.selectbox(
  'Select Policy type',
  ('star health', 'HDFC', 'ICICI')
)
if option:
  #Getting pdf input.
  uploaded_pdf = st.file_uploader("Upload your pdf")
  if uploaded_pdf is not None:
    url = "https://pivot-port-poldoc-health.attributum.com/api/ml_process"
    files = {
      "input_file" : uploaded_pdf
    } 
    data = {
      "insurance_company" : option.lower(),
      "data_type" : "Generic"
    }
    headers = {"Authorization": st.secrets["auth_key"]}

    #Post API call.
    response = requests.post(url, files=files, data=data, headers=headers)

    if response:
      show_table(response.json())

